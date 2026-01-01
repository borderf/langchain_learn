"""
deepagent: planning, file system, subagent
demo: research report
uv add deepagents

过程：
内置的工具：write_todos, todo list
internet_search, update todo list status
内置的工具：write_file, 写报告
"""

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from tavily import TavilyClient
from typing import Literal
from dotenv import load_dotenv

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
        topic=topic,
        include_raw_content=include_raw_content,
    )


RESEARCH_INSTRUCTIONS = """
你是一个专业的研究员。你的任务是进行彻底的研究并撰写一份完整的报告。
你可以使用以下工具：
- internet_search: 用于搜索互联网信息
请确保：
1.进行全面的搜索来收集信息
2.验证信息的准确性
3.组织信息并撰写结构化的报告
4.务必生成报告到当前的文件夹下
"""

model = init_chat_model(
    model="deepseek-ai/DeepSeek-V3.2",
    model_provider="openai",
    temperature=0.1,
)

deep_agent = create_deep_agent(
    model=model,
    system_prompt=RESEARCH_INSTRUCTIONS,
    tools=[internet_search],
)

query = "什么是资产减值？详细介绍一下它"

for event in deep_agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    if "files" in event:
        print(event["files"])
    event["messages"][-1].pretty_print()
