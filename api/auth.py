from fastapi import APIRouter, HTTPException, status
from models import UserCreate, UserResponse, UserLogin, UserLoginResponse
from service import auth_signup, auth_signin

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/sign-in", response_model=UserLoginResponse)
async def auth_signin_enpoint(user: UserLogin):
    result = auth_signin(user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Kombinasi username atau password salah. Silakan coba lagi.")
    return result

@router.post("/sign-up", response_model=UserResponse)
async def auth_signup_endpoint(user: UserCreate):
    return auth_signup(user)
