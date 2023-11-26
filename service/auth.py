from database.connection import database
from datetime import datetime
from utils import hash_password, generate_token, verify_password
from typing import Optional, List
from pymongo.results import DeleteResult
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from utils import verify_token
from fastapi import status, HTTPException, Depends
from dto import error_response
import re
import pytz
import uuid
import os

from models import (
    UserCreate,
    UserUpdate,
    UserDeleteResponse, 
    UserResponse,
    UserLogin,
    UserLoginResponse
)


collection = database["users"]
SECRET_KEY = os.getenv('SECRET_KEY')

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Tidak dapat memvalidasi token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = verify_token(token, SECRET_KEY)
    
    if user is None:
        raise credentials_exception
    
    user_data = collection.find_one({"id": user["id"]})
    user["role"] = user_data["role"]
    user["created_at"] = user_data["created_at"]
    user["updated_at"] = user_data["updated_at"]
    return user

# Use a regular expression to validate email format
def is_email_valid(email: str) -> bool:
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_regex, email))

def is_email_registered(email: str) -> bool:
    return collection.find_one({"email": email}) is not None

def is_username_registered(username: str) -> bool:
    return collection.find_one({"username": username}) is not None

# Password must have at least 6 characters, 1 uppercase, and a mix of letters and numbers
def is_password_valid(password: str) -> bool:
    return len(password) >= 6 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)

def auth_signin(user: UserLogin) -> Optional[UserLoginResponse]:
    user_dict = user.dict()
    username = user_dict["username"]
    password = user_dict["password"]
    
    data = get_user_by_username(username)
    if data is None:
        return None
    
    payload = {
        'id': data["id"],
        'email': data["email"],
        'username': data["username"],
    }
    
    user_data = {
        'status': 401,
        'message': 'Unauthorized: Kombinasi username/password salah. Silakan coba lagi.',
        'token': ""
    }
    
    is_password_valid = verify_password(password, data["password"])
    if is_password_valid: 
        token = generate_token(SECRET_KEY, payload)
        user_data["status"] = 200
        user_data["message"] = "success"
        user_data["token"] = token
        
    return UserLoginResponse(result=user_data)

def auth_signin_token(user: OAuth2PasswordRequestForm) -> Optional[UserLoginResponse]:
    username = user.username
    password = user.password
    
    data = get_user_by_username(username)
    if data is None:
        return None
    
    payload = {
        'id': data["id"],
        'email': data["email"],
        'username': data["username"],
    }
    
    user_data = {
        'access_token': '',
        'token_type': "bearer"
    }
    
    is_password_valid = verify_password(password, data["password"])
    if is_password_valid: 
        token = generate_token(SECRET_KEY, payload)
        user_data["access_token"] = token
        
    return user_data

def auth_signup(user: UserCreate) -> UserResponse:
     # Validate email format
    if not is_email_valid(user.email):
        return error_response("Invalid email format", 400)

    # Check if the email is already registered
    if is_email_registered(user.email):
        return error_response("Email is already registered", 400)
    
    # Validate password format
    if not is_password_valid(user.password):
        return error_response("Invalid password format. It must have at least 6 characters, 1 uppercase letter, and a mix of letters and numbers.", 400)
    
     # Check if the username is already registered
    if is_username_registered(user.username):
        return error_response("Username is already taken", 400)

    user_dict = user.dict()
    user_dict["id"] = str(uuid.uuid4())
    if user_dict["role"] != "teacher":
        user_dict["role"] = "user"
    password = user_dict["password"]
    hashed_password = hash_password(password)
    user_dict["password"] = hashed_password
    created_at = datetime.now(pytz.timezone("Asia/Jakarta"))
    user_dict["created_at"] = created_at
    user_dict["updated_at"] = created_at
    collection.insert_one(user_dict)
    new_user = UserResponse(**user_dict)

    return new_user

def get_users() -> List[UserResponse]:
    try:
        users_data = list(collection.find())
        users = [UserResponse(**user_data) for user_data in users_data]
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def get_user_by_username(username: str):
    user_data = collection.find_one({"username": username})
    if not user_data:
        return None
    
    return user_data

def get_user(id: str):
    user_data = collection.find_one({"id": id})
    if not user_data:
        return None
    
    return user_data

def update_user(user_id: str, updated_user: UserUpdate) -> UserResponse:
    updated_dict = updated_user.dict()
    
    password = updated_dict["password"]
    hashed_password = hash_password(password)
    updated_dict["password"] = hashed_password

    updated_dict["updated_at"] = datetime.now(pytz.timezone("Asia/Jakarta"))

    result = collection.update_one({"id": user_id}, {"$set": updated_dict})
    if result.modified_count == 0:
        return None
    user_data = collection.find_one({"id": user_id})
    return UserResponse(**user_data) if user_data else None

def delete_user(user_id: str) -> Optional[UserDeleteResponse]:
    result: DeleteResult = collection.delete_one({"id": user_id})
    if result.deleted_count == 0:
        return None

    return UserDeleteResponse(message=f"{result.deleted_count} User berhasil dihapus")