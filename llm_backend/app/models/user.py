from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)#index=True = 给数据库表额外建一个普通索引，提高查询效率
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="active")

    # 关系示例（如果有其他表关联）
    # posts = relationship("Post", back_populates="owner")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")