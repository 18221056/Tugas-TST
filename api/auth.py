from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserCreate, UserResponse, UserLogin, UserLoginResponse, UserGetMeResponse
from service import auth_signup, auth_signin, auth_signin_token, get_current_user

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

@router.post("/token")
async def auth_signin_enpoint(user: OAuth2PasswordRequestForm = Depends()):
    result = auth_signin_token(user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Kombinasi username atau password salah. Silakan coba lagi.")
    return result

@router.get("/me", response_model=UserGetMeResponse)
async def get_me_enpoint(current_user: UserResponse = Depends(get_current_user)):
    return current_user
    
