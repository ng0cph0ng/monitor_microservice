from fastapi import FastAPI, HTTPException

app = FastAPI()

inventory = {"item_1": 10, "item_2": 5}

@app.get("/")
def home():
    return {"message": "Inventory service is running"}

@app.get("/inventory")
def check_inventory(item: str = None):
    if item and item not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"items": list(inventory.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

