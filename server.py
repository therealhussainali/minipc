from fastapi import FastAPI, HTTPException
import pymysql
from pydantic import BaseModel

# Database connection
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_root_password",
    "database": "user_auth",
}

app = FastAPI()

# User model for input validation
class User(BaseModel):
    username: str
    password: str

# Route to get all users (⚠️ Unsafe in real-world apps)
@app.get("/users")
def get_users():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users")
        users = cursor.fetchall()
        conn.close()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to add a new user
@app.post("/add_user")
def add_user(user: User):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
        conn.commit()
        conn.close()
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
