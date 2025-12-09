from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.user_service import UserService
from app.core.security import create_access_token, get_current_user
from app.models.user import User
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/register",response_model = UserResponse)
async def register(user: UserCreate,db: AsyncSession = Depends(get_db))-> User:
    """用户注册接口"""  
    try :
        user_service = UserService(db)
        new_user = await user_service.create_user(user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/token",response_model = Token)
async def login(user: UserLogin,db:AsyncSession = Depends(get_db)):
    """用户登录接口"""
    user_service = UserService(db)
    authenticated_user = await user_service.authenticate_user(user.email,user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401,detail="无效的邮箱或密码")
    # 生成并返回 token （这里简化处理，实际应用中应生成 JWT 或其他类型的 token）
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("users/me",response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user
