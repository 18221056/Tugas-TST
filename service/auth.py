from models import (
    UserCreate,
    UserUpdate,
    UserDeleteResponse, 
    UserResponse,
    UserLogin,
    UserLoginResponse
)

from database.connection import database
from datetime import datetime
import pytz
import uuid
from utils import hash_password, generate_token, verify_password
from typing import Optional, List
from pymongo.results import DeleteResult

collection = database["users"]

def auth_signin(user: UserLogin) -> Optional[UserLoginResponse]:
    user_dict = user.dict()
    email = user_dict["email"]
    password = user_dict["password"]
    
    data = get_user_by_email(email)
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
        token = generate_token("secret_key", payload)
        user_data["status"] = 200
        user_data["message"] = "success"
        user_data["token"] = token
        
        # Simpan token dalam session
        # session["token"] = token
        
    return UserLoginResponse(result=user_data)

def auth_signup(user: UserCreate) -> UserResponse:
    user_dict = user.dict()
    user_dict["id"] = str(uuid.uuid4())
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

def get_user_by_email(email: str):
    user_data = collection.find_one({"email": email})
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
