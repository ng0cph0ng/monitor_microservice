from fastapi import FastAPI, HTTPException

app = FastAPI()

# Dữ liệu kho hàng
inventory = {
    "item_1": {"quantity": 10, "price": 10},
    "item_2": {"quantity": 5, "price": 20},
    "item_3": {"quantity": 8, "price": 15}
}

@app.get("/inventory")
def get_item(item: str):
    if item not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item, "quantity": inventory[item]["quantity"], "price": inventory[item]["price"]}

@app.post("/inventory")
def update_inventory(item: str, quantity: int):
    if item not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    if inventory[item]["quantity"] < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    inventory[item]["quantity"] -= quantity
    return {"item": item, "remaining_quantity": inventory[item]["quantity"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

