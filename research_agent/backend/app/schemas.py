"""
输入输出的模型定义
"""
from datetime import datetime
from typing import Optional, List, Generic, TypeVar, Any, Dict

from pydantic import BaseModel, ConfigDict

T = TypeVar('T')


# 分页参数
class PageParams(BaseModel):
    page: int = 1
    page_size: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


# 分页响应
class PageResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(cls, items: List[T], total: int, page_params: PageParams) -> 'PageResponse[T]':
        total_pages = (total + page_params.page_size - 1) // page_params.page_size
        return cls(
            items=items,
            total=total,
            page=page_params.page,
            page_size=page_params.page_size,
            total_pages=total_pages
        )


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
    update_at: Optional[datetime]


# 消息更新请求
class MessageUpdate(BaseModel):
    content: Optional[str] = None


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


# 聊天请求
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None
    stream: Optional[bool] = False


# 聊天响应
class ChatResponse(BaseModel):
    session_id: int
    message: MessageResponse
    is_complete: bool = True


# 流式响应块
class ChatStreamChunk(BaseModel):
    content: str
    is_final: bool = False
    tool_calls: Optional[List[Dict[str, Any]]] = None
