"""
数据表增删改查操作
"""
import datetime
from typing import Annotated, Optional, List

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import ChatSession, ChatMessages
from schemas import SessionCreate, SessionUpdate, MessageCreate, MessageUpdate, PageParams, PageResponse

# ===============会话操作函数=====================
SessionDep = Annotated[Session, Depends(get_session)]


def create_session(session_data: SessionCreate, session: SessionDep) -> ChatSession:
    """创建新的聊天会话"""
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
    """获取所有聊天会话（分页）"""
    statement = select(ChatSession).where(ChatSession.is_deleted == False)
    items = session.exec(statement).all()
    return items


def get_session_with_messages(session_id: int, session: SessionDep, page_params: PageParams = PageParams()) -> Optional[
    dict]:
    """获取聊天会话及其所有消息（分页）"""
    chat_session = get_session(session_id, session)
    if not chat_session:
        return None
    messages = get_messages_by_session(session_id, session, page_params)
    return {
        "session": chat_session,
        "messages": messages
    }


def list_sessions_with_messages(session: SessionDep, page_params: PageParams = PageParams(),
                                messages_limit: Optional[int] = None) -> PageResponse[dict]:
    """获取所有聊天会话及其消息（分页）"""
    count_statement = select(ChatSession).where(ChatSession.is_deleted == False)
    total = len(session.exec(count_statement).all())

    statement = select(ChatSession).where(ChatSession.is_deleted == False).order_by(
        ChatSession.update_at.desc()).offset(page_params.offset).limit(page_params.limit)
    sessions = session.exec(statement).all()

    result = []
    for chat_session in sessions:
        if messages_limit:
            message_statement = select(ChatMessages).where(
                ChatMessages.session_id == chat_session.id,
                ChatMessages.is_deleted == False
            ).order_by(ChatMessages.create_at.asc()).limit(messages_limit)
            messages = session.exec(message_statement).all()
        else:
            messages = get_messages_by_session(chat_session.id, session).items
        result.append({
            "session": chat_session,
            "messages": messages
        })

    return PageResponse.create(result, total, page_params)


def update_session(session_id: int, update_data: SessionUpdate, session: SessionDep) -> ChatSession:
    """更新会话信息"""
    chat_session = get_session(session_id, session)
    if not chat_session:
        raise HTTPException(status_code=404, detail="会话不存在")
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    if update_dict:
        for key, value in update_dict.items():
            if hasattr(chat_session, key):
                setattr(chat_session, key, value)
        session.add(chat_session)
        session.commit()
        session.refresh(chat_session)
    return chat_session


def delete_session(session_id: int, session: SessionDep) -> bool:
    """删除聊天会话（软删除）"""
    chat_session = get_session(session_id, session)
    if not chat_session:
        raise HTTPException(status_code=404, detail="会话不存在")
    chat_session.is_deleted = True
    session.add(chat_session)
    session.commit()
    return True


# ===============消息操作函数=====================


def create_message(message_data: MessageCreate, session: SessionDep) -> ChatMessages:
    """创建新的聊天消息"""
    chat_session = get_session(message_data.session_id, session)
    if not chat_session:
        raise HTTPException(status_code=500, detail="会话不存在")
    db_message = ChatMessages(
        session_id=message_data.session_id,
        role=message_data.role,
        content=message_data.content
    )
    chat_session.update_at = datetime.now()
    session.add(chat_session)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


def get_message(message_id: int, session: SessionDep) -> Optional[ChatMessages]:
    """获取聊天消息"""
    return session.get(ChatMessages, message_id)


def get_messages_by_session_all(session_id: int, session: SessionDep) -> List[ChatMessages]:
    """获取会话的所有消息"""
    statement = select(ChatMessages).where(ChatMessages.session_id == session_id,
                                           ChatMessages.is_deleted == False).order_by(ChatMessages.create_at.desc())
    return session.exec(statement).all()


def get_messages_by_session(session_id: int, session: SessionDep, page_params: PageParams = PageParams()) -> \
        PageResponse[ChatMessages]:
    """获取指定会话的所有消息（分页）"""
    count_statement = select(ChatMessages).where(
        ChatMessages.session_id == session_id,
        ChatMessages.is_deleted == False
    )
    total = len(session.exec(count_statement).all())

    statement = select(ChatMessages).where(
        ChatMessages.session_id == session_id,
        ChatMessages.is_deleted == False
    ).order_by(ChatMessages.create_at.asc()).offset(page_params.offset).limit(page_params.limit)
    items = session.exec(statement).all()

    return PageResponse.create(items, total, page_params)


def list_messages(session: SessionDep, page_params: PageParams = PageParams()) -> PageResponse[ChatMessages]:
    """获取所有聊天消息（分页）"""
    count_statement = select(ChatMessages).where(ChatMessages.is_deleted == False)
    total = len(session.exec(count_statement).all())

    statement = select(ChatMessages).where(ChatMessages.is_deleted == False).order_by(
        ChatMessages.create_at.desc()).offset(page_params.offset).limit(page_params.limit)
    items = session.exec(statement).all()

    return PageResponse.create(items, total, page_params)


def delete_message(message_id: int, session: SessionDep) -> bool:
    """删除聊天消息（软删除）"""
    message = get_message(message_id, session)
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    message.is_deleted = True
    session.commit()
    return True


def update_message(message_id: int, update_data: MessageUpdate, session: SessionDep) -> ChatMessages:
    """更新聊天消息"""
    message = get_message(message_id, session)
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    if update_dict:
        for key, value in update_dict.items():
            if hasattr(message, key):
                setattr(message, key, value)
        session.add(message)
        session.commit()
        session.refresh(message)
    return message


def delete_messages_by_session(session_id: int, session: SessionDep) -> int:
    """删除指定会话的所有消息（软删除）"""
    messages = get_messages_by_session(session_id, session)
    for message in messages:
        message.is_deleted = True
    session.commit()
    return len(messages)
