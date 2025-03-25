from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()
USER_DATA_FILE = "/app/users.json"

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {"valid": {}, "invalid": {}}
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.post("/users")
def create_user(user_id: str, valid: bool, balance: int):
    users = load_users()
    group = "valid" if valid else "invalid"
    if user_id in users["valid"] or user_id in users["invalid"]:
        raise HTTPException(status_code=400, detail="User already exists")
    users[group][user_id] = {"balance": balance}
    save_users(users)
    return {"message": "User created successfully", "user_id": user_id}

@app.put("/users/{user_id}/balance")
def update_user_balance(user_id: str, amount: int):
    users = load_users()
    for group in ["valid", "invalid"]:
        if user_id in users[group]:
            if users[group][user_id]["balance"] < amount:
                raise HTTPException(status_code=402, detail="Insufficient funds")
            users[group][user_id]["balance"] -= amount
            save_users(users)
            return {"user_id": user_id, "new_balance": users[group][user_id]["balance"]}
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}/change_group")
def change_user_group(user_id: str):
    users = load_users()
    for group in ["valid", "invalid"]:
        if user_id in users[group]:
            new_group = "invalid" if group == "valid" else "valid"
            users[new_group][user_id] = users[group].pop(user_id)  # Chuyển user sang nhóm mới
            save_users(users)
            return {"user_id": user_id, "new_group": new_group}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
w
