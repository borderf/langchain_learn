"""
输入输出的模型定义
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


# 消息基类
class MessageBase(BaseModel):
    role: str
    content: str
    session_id: int

    # 允许从 ORM 实例（SQLModel模型）创建Pydantic模型
    model_config = ConfigDict(from_attributes=True)


# 消息创建请求
class MessageCreate(MessageBase):
    pass


# 消息响应
class MessageResponse(MessageBase):
    id: int
    create_at: datetime


# 会话基类
class SessionBase(BaseModel):
    title: Optional[str] = "新的会话"

    # 允许从ORM实例创建
    model_config = ConfigDict(from_attributes=True)


# 会话创建请求
class SessionCreate(SessionBase):
    pass

# 会话更新请求
class SessionUpdate(BaseModel):
    title: Optional[str] = None


class SessionResponse(SessionBase):
    id: int
    create_at: datetime
    update_at: Optional[datetime]
    messages: List[MessageResponse] = []
