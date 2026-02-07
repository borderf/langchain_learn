import os
from datetime import datetime
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Literal
from langgraph.types import Command as _Command


load_dotenv()

tavily_client = TavilyClient()


@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query=query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


SYSTEM_PROMPT = """
你是一个智能助手，你的任务是帮助用户完成各种任务。
你可以使用互联网搜索工具来获取信息。
## `internet_search`
使用此工具对给定查询进行互联网搜索，你可以指定返回结果的最大数量、主题以及是否包含原始内容。

今天的日期是：{today}
"""

checkpointer = MemorySaver()

model = init_chat_model(
    model="deepseek-ai/DeepSeek-V3.2",
    model_provider="openai",
    temperature=0.1,
)

agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[internet_search],
    checkpointer=checkpointer,
    interrupt_on={"internet_search": True},
)

# 多轮循环对话
printed_msg_ids = set()
thread_id = "user_session_001"
# 配置会话
config = {"configurable": {"thread_id": thread_id}}
print("开始对话（输入'exit'退出）：")
while True:
    user_input = input("\n用户: ").strip()
    if user_input.lower() == "exit":
        break

    # 使用 values 模式多次返回完整状态，这里按 message.id 去重，并按类型分类打印
    pending_resume = None
    while True:
        if pending_resume is None:
            request = {"messages": [{"role": "user", "content": user_input}]}
        else:
            request = _Command(resume=pending_resume)
            pending_resume = None

        for item in agent.stream(
            request,
            config=config,
            stream_mode="values",
        ):
            state = item[0] if isinstance(item, tuple) and len(item) == 2 else item
