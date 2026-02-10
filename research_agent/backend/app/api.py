"""
前端接口服务
"""
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.database import get_session
from app.schemas import SessionResponse, SessionCreate, SessionUpdate, MessageResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])

SessionDep = Annotated[Session, Depends(get_session)]


# ========= 会话管理 ===============
@router.post("/session/create", response_model=SessionResponse)
async def create_session(session_data: SessionCreate, session: SessionDep):
    """创建新的聊天会话"""
    chat_session = crud.create_session(session_data, session)
    return chat_session


@router.post("/session/list", response_model=List[SessionResponse])
async def get_sessions(session_id: int, session: SessionDep):
    """获取会话信息"""
    chat_session = crud.get_session(session_id, session)
    if not chat_session:
        raise HTTPException(status_code=500, detail="Session not found")

    # 获取会话消息
    chat_messages = crud.get_messages_by_session_all(session_id, session)
    chat_session.messages = chat_messages
    return chat_session


@router.post("/session/update", response_model=SessionResponse)
async def update_session(session_id: int, update_data: SessionUpdate, session: SessionDep):
    """更新会话消息"""
    chat_session = crud.get_session(session_id, session)
    if not chat_session:
        raise HTTPException(status_code=500, detail="Session not found")
    updated_session = crud.update_session(session_id, update_data, session)
    if not updated_session:
        raise HTTPException(status_code=500, detail="Failed to update session")
    # 获取会话消息
    messages = crud.get_messages_by_session_all(session_id, session)
    updated_session.messages = messages
    return updated_session


@router.post("/session/delete")
async def delete_session(session_id: int, session: SessionDep):
    """删除会话"""
    success = crud.delete_session(session_id, session)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete session")
    return {"message": "Session deleted"}


@router.get("/session/messages", response_model=List[MessageResponse])
async def get_sessions_messages(session_id: int, session: SessionDep):
    """获取会话的所有消息"""
    messages = crud.get_messages_by_session_all(session_id, session)
    return messages

# ========== 消息处理 ==============
# @router.post("/message/send", response_model=MessageResponse)
