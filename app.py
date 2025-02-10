from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
import sqlite3
import secrets
import os
from typing import Optional

# Secret key for JWT (should be stored securely)
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

class GeometricPasswordSystem:
    def __init__(self):
        self.patterns = {
            'square': ['WSED', 'QWER', 'ASDF'],
            'triangle': ['WSD', 'QWE', 'ASD'],
            'line': ['QAZ', 'WSX', 'EDC']
        }
        self.special_chars = ['#', '@', '$', '&']
        
    def generate_password(self, base_pattern: str, service: str, month: str) -> str:
        return f"{base_pattern}-{service[0].upper()}{self.special_chars[0]}{month[0].upper()}"
    
    def validate_pattern(self, pattern: str) -> bool:
        return any(pattern in patterns for patterns in self.patterns.values())

def get_db_connection():
    conn = sqlite3.connect('passwords.db')
    conn.row_factory = sqlite3.Row
    return conn

# User Model
class User(BaseModel):
    username: str
    email: str
    base_pattern: str

# Service Model
class Service(BaseModel):
    name: str
    url: Optional[str] = None

# Secure Password Hashing (PBKDF2)
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# JWT Token Generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Initialize Database
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        username TEXT, 
        email TEXT, 
        base_pattern TEXT)
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY, 
        user_id INTEGER, 
        service TEXT, 
        hashed_pattern TEXT, 
        created_at TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if not password_system.validate_pattern(user.base_pattern):
        raise HTTPException(status_code=400, detail="Invalid pattern")
    
    hashed_pattern = hash_password(user.base_pattern)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, base_pattern) VALUES (?, ?, ?)", (user.username, user.email, hashed_pattern))
    conn.commit()
    conn.close()
    return {"message": "User created successfully"}

@app.post("/generate_password/")
async def generate_password(service: Service, user_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT base_pattern FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    current_month = datetime.now().strftime("%B")
    password = password_system.generate_password(user["base_pattern"], service.name, current_month)
    hashed_password = hash_password(password)
    
    c.execute("INSERT INTO passwords (user_id, service, hashed_pattern, created_at) VALUES (?, ?, ?, ?)",
              (user_id, service.name, hashed_password, datetime.now()))
    conn.commit()
    conn.close()
    
    return {"service": service.name, "password": "Generated Securely", "created_at": datetime.now()}

@app.post("/token/")
async def login(username: str, base_pattern: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, base_pattern FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if not user or not verify_password(base_pattern, user["base_pattern"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
