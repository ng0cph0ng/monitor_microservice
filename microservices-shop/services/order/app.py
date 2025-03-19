from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

AUTH_URL = "http://auth:8004/auth"
INVENTORY_URL = "http://inventory:8003/inventory"
PAYMENT_URL = "http://payment:8002/payments"

@app.get("/")
def home():
    return {"message": "Order service is running"}

@app.get("/orders")
def get_orders():
    return {"orders": ["order1", "order2"]}

@app.post("/create")
def create_order(user_id: str, item: str):
    auth_response = requests.get(AUTH_URL, params={"user_id": user_id})

    if auth_response.status_code != 200:
        raise HTTPException(status_code=403, detail="Authentication failed")

    inventory_response = requests.get(INVENTORY_URL)
    if inventory_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Item out of stock")

    payment_response = requests.get(PAYMENT_URL)
    if payment_response.status_code != 200:
        raise HTTPException(status_code=402, detail="Payment failed")

    return {"message": f"Order for {item} placed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

