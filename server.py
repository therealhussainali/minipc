from fastapi import FastAPI, HTTPException
import pymysql
from pydantic import BaseModel

# Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1223",
    "database": "user_auth",
    "cursorclass": pymysql.cursors.DictCursor,  # Returns results as dictionaries
}

app = FastAPI()

# User model for input validation
class User(BaseModel):
    username: str
    password: str

# Route to get all users (⚠️ Exposes passwords, use only for testing)
@app.get("/users")
def get_users():
    try:
        with pymysql.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT username, password FROM users")
                users = cursor.fetchall()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to add a new user
@app.post("/add_user")
def add_user(user: User):
    try:
        with pymysql.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
                conn.commit()
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
