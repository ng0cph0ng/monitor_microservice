from fastapi import FastAPI, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import requests

app = FastAPI()
AUTH_URL = "http://auth:8004/auth"
INVENTORY_URL = "http://inventory:8003/inventory"

orders = {}  # Lưu đơn hàng
order_counter = 1  # Biến đếm số lượng đơn hàng

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/create")
def create_order(user_id: str, item: str, quantity: int):
    global order_counter

    # Xác thực người dùng
    auth_response = requests.get(AUTH_URL, params={"user_id": user_id})
    if auth_response.status_code != 200:
        raise HTTPException(status_code=403, detail="Authentication failed")

    # Kiểm tra kho hàng
    inventory_response = requests.post(INVENTORY_URL, params={"item": item, "quantity": quantity})
    if inventory_response.status_code != 200:
        raise HTTPException(status_code=inventory_response.status_code, detail=inventory_response.json()["detail"])

    # Tạo order_id
    order_id = f"order_{order_counter}"
    order_counter += 1

    # Lưu đơn hàng
    orders[order_id] = {"user_id": user_id, "item": item, "quantity": quantity, "status": "confirmed"}
    
    return {"order_id": order_id, "message": "Order placed successfully"}

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

