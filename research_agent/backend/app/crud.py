"""
数据表增删改查操作
"""
from typing import Annotated, Optional, List

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import ChatSession
from schemas import SessionCreate, SessionUpdate

# ===============会话操作函数=====================
SessionDep = Annotated[Session, Depends(get_session)]


def create_session(session_data: SessionCreate, session: SessionDep) -> ChatSession:
    """创建新的聊天会话"""
    # 设置默认标题
    title = session_data.title if session_data.title else "新的会话"

    db_session = ChatSession(title=title)
    session.add(db_session)
    session.commit()
    session.refresh(db_session)
    return db_session


def get_session(session_id: int, session: SessionDep) -> Optional[ChatSession]:
    """获取聊天会话"""
    return session.get(ChatSession, session_id)


def list_sessions(session: SessionDep) -> List[ChatSession]:
    """获取所有聊天会话"""
    statement = select(ChatSession).order_by(ChatSession.update_at.desc())
    return session.exec(statement).all()

def update_session(session_id: int, update_data: SessionUpdate, session: SessionDep) -> ChatSession:
    """更新会话信息"""
    chat_session = get_session(session_id, session)
    if not chat_session:
        raise HTTPException(status_code=500, detail="会话不存在")
    # todo 更新时判断只更新有值的属性