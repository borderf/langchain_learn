"""
针对数据库的操作
"""
from sqlmodel import create_engine, Session
from app.config import settings

from models import SQLModel

engine = create_engine(settings.database_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


# 可以多次调用
# 1.首次调用时创建数据库数据表
# 2.之后的调用不会重复创建
def get_session():
    with Session(engine) as session:
        yield session
