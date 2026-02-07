import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行的代码
    logger.info("App启动...")
    create_tables()  # 创建数据库和数据表
    yield
    # 应用关闭时执行的代码
    logger.info("App关闭...")


app = FastAPI(
    title="Research Agent",
    description="超牛的研究智能体",
    version="0.0.1",
    lifespan=lifespan,
)
