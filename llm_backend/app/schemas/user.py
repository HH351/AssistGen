from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str  

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    status: str
    class Config:
        orm_mode = True
# ✅ API 层返回数据结构
# ✅ 可控字段集合
# ✅ 自动做「序列化 + 校验 + 剔除多余字段」
# ✅ 安全（明确不包含 password_hash） 所以肯定和app.models.user.User区分开