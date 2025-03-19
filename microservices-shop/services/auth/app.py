from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

@app.get("/auth")
def authenticate(user_id: str = Query(...)):
    if user_id != "valid_user":
        raise HTTPException(status_code=403, detail="Authentication failed")

    return {"status": "Authenticated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

