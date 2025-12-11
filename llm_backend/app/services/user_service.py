from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.user import User
from typing import Optional
from app.schemas.user import UserCreate
from app.core.logger import get_logger
from app.core.hashing import get_password_hash,verify_password

logger = get_logger(service = "user_service")

class UserService:
    def __init__(self,db: AsyncSession):
        self.db = db

    async def create_user(self,user_create: UserCreate) -> Optional[User]:
        """创建新用户"""
        query =  select(User).where(
            or_(
                User.username == user_create.username,
                User.email == user_create.email
            )
        )
        result = await self.db.execute(query)
        existing_user = result.scalar_one_or_none()
        logger.info(f"Checking existing user for username: {user_create.username}, email: {user_create.email}")
        if existing_user:
            if existing_user.username == user_create.username:
                raise ValueError("该用户名已经被注册！")
            else:
                raise ValueError("该邮箱已经被注册！")
          
        
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=get_password_hash(user_create.password)
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        logger.info(f"Created new user: {new_user.username}")
        return new_user

    async def get_user_by_id(self,user_id:int) -> Optional[User]:
        """通过用户ID获取用户"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        验证用户
        password: 前端传来的 SHA256 哈希密码
        """
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()  # 获取查询结果中的第一个用户，如果存在则返回，否则返回 None
        logger.info(f"Authenticating user with email: {email}")
        if not user:
            logger.warning(f"User not found: {email}")
            return None

        if not verify_password(password, user.password_hash):
            logger.warning(f"Invalid password for user: {email}")
            
            print("验证失败")
            return None
        return user
        
    async def get_user_by_username(self,username:str) -> Optional[User]:
        """通过用户名获取用户"""
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user