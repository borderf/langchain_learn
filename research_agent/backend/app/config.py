"""
配置类
"""
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # 模型配置
    api_key: str = os.getenv('OPENAI_API_KEY', '')
    model: str = os.getenv('OPENAI_MODEL', 'Qwen/Qwen3-8B')
    base_url: str = os.getenv('OPENAI_BASE_URL', 'https://api.siliconflow.cn/v1')

    # 数据库配置
    database_url: str = os.getenv('DATABASE_URL', 'mysql+pymysql://root:123456@localhost/langchain?charset=utf8')

    # 服务器配置
    host: str = os.getenv('HOST', '0.0.0.0')
    port: int = int(os.getenv('PORT', '8080'))

    # Agent配置
    agent_temperature: float = float(os.getenv('AGENT_TEMPERATURE', '0.1'))
    agent_max_tokens: int = int(os.getenv('AGENT_MAX_TOKENS', '2000'))

    class Config:
        env_file = '.env'


settings = Settings()
