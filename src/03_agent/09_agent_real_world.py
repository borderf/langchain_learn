"""
创建一个现实的更复杂的agent的例子
langchain官网的示例
大模型：model
系统提示词：system_prompt
工具：tools，用户传递参数
    工具运行时上下文传递参数：context_schema
记忆管理：checkpointer
结构化输出：response_format
"""
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime

from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# 系统提示词
SYSTEM_PROMT = """你是一个专业的天气预报专家，
"""
