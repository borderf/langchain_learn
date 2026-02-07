"""
定义会话的数据结构
"""

from datetime import datetime

from snowflake import SnowflakeGenerator
from sqlalchemy import Column, func, BOOLEAN, String
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlmodel import SQLModel, Field

# 雪花算法生成器
gen = SnowflakeGenerator(66)


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_session"

    id: int | None = Field(
        default_factory=lambda: next(gen),
        primary_key=True,
        sa_column_kwargs={"autoincrement": False},
        index=True,
    )
    title: str = Field(default="新的会话", sa_column=Column(String(100), server_default="New Session", nullable=False))
    create_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now(), nullable=False))
    update_at: datetime = Field(
        sa_column=Column(TIMESTAMP, server_default=func.now(), nullable=False, onupdate=func.now()))
    is_deleted: bool = Field(default=False, sa_column=Column(BOOLEAN, server_default="0", nullable=False))


class ChatMessages(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: int | None = Field(
        default_factory=lambda: next(gen),
        primary_key=True,
        sa_column_kwargs={"autoincrement": False},
        index=True,
    )
    session_id: int = Field(nullable=False, index=True)
    role: str = Field(max_length=50, nullable=False)
    content: str | None
    create_at: datetime = Field(sa_column=Column(TIMESTAMP, server_default=func.now(), nullable=False))
    update_at: datetime = Field(
        sa_column=Column(TIMESTAMP, server_default=func.now(), nullable=False, onupdate=func.now()))
    is_deleted: bool = Field(default=False, sa_column=Column(BOOLEAN, server_default="0", nullable=False))
