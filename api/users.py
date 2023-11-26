from fastapi import APIRouter, HTTPException, status
from models import UserUpdate, UserResponse, UserDeleteResponse
from typing import List
from pydantic import ValidationError
from service import delete_user, update_user, get_users, get_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("", response_model=List[UserResponse])
async def get_users_enpoint():
    result = get_users()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")
    return result

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_enpoint(user_id: str):
    result = get_user(user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")
    return result

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: str, updated_user: UserUpdate):
    try:
        result = update_user(user_id, updated_user)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")
        return result
    except ValidationError as e:
        print(e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validasi error")

@router.delete("/{user_id}", response_model=UserDeleteResponse)
async def delete_user_endpoint(user_id: str):
    result = delete_user(user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")
    return result