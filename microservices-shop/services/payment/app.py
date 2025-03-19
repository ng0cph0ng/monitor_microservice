from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Payment service is running"}

@app.get("/payments")
def process_payments():
    return {"status": "Payment successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

