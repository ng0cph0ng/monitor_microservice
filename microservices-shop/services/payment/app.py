from fastapi import FastAPI, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import requests

app = FastAPI()
AUTH_SERVICE_URL = "http://auth:8004/users"
ORDER_SERVICE_URL = "http://order:8001/orders"
INVENTORY_SERVICE_URL = "http://inventory:8003/inventory"

# Lưu trạng thái thanh toán của mỗi đơn hàng và số dư của người dùng
paid_orders = {}
user_balances = {}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/payments")
def process_payment(order_id: str):
    # Kiểm tra nếu đơn hàng đã được thanh toán
    if order_id in paid_orders:
        raise HTTPException(status_code=400, detail="Order already paid")

    # Lấy thông tin đơn hàng
    order_response = requests.get(f"{ORDER_SERVICE_URL}/{order_id}")
    if order_response.status_code != 200:
        raise HTTPException(status_code=404, detail="No valid order found")
    
    order_data = order_response.json()
    user_id = order_data["user_id"]
    item = order_data["item"]
    quantity = order_data["quantity"]

    # Lấy thông tin giá sản phẩm từ inventory
    inventory_response = requests.get(f"{INVENTORY_SERVICE_URL}?item={item}")
    if inventory_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get item price")

    item_price = inventory_response.json().get("price", 0)
    amount = item_price * quantity  # Tính tổng tiền

    # Kiểm tra và cập nhật số dư người dùng
    if user_id not in user_balances:
        user_response = requests.get(f"{AUTH_SERVICE_URL}/{user_id}")
        if user_response.status_code != 200:
            raise HTTPException(status_code=403, detail="User not found or unauthorized")
        user_balances[user_id] = user_response.json()["balance"]

    if user_balances[user_id] < amount:
        raise HTTPException(status_code=402, detail="Insufficient funds")

    user_balances[user_id] -= amount  # Trừ tiền
    paid_orders[order_id] = True  # Đánh dấu đã thanh toán

    return {"status": "Payment successful", "remaining_balance": user_balances[user_id]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
