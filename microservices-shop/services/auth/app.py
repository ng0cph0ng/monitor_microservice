from fastapi import FastAPI, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import json
import os
import requests

app = FastAPI()
USER_DATA_FILE = "/app/users.json"

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        raise HTTPException(status_code=500, detail="Failed to load user data")
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

@app.get("/auth")
def authenticate(user_id: str):
    users = load_users()
    if user_id in users.get("valid", {}):
        return {"status": "Authenticated"}
    elif user_id in users.get("invalid", {}):
        raise HTTPException(status_code=403, detail="Authentication failed")
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/{user_id}")
def get_user(user_id: str):
    users = load_users()
    for group in ["valid", "invalid"]:
        if user_id in users[group]:
            return {"user_id": user_id, "balance": users[group][user_id]["balance"], "valid": group == "valid"}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

