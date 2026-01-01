"""
agent使用tavily实现网络搜索
tavily：搜索引擎，给agent用的，提供两种api：
    - tavily-search
    - tavily_extract
https://www.tavily.com，注册，自动获取 TAVILY_API_KEY=...
放到.env里面，免费额度：1000次/月

uv add tavily-python langchain-tavily
"""

from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Literal

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
你是一个专业的研究员。你的任务是进行彻底的研究并撰写一份完整的报告。
你可以使用以下工具：
- internet_search: 用于搜索互联网信息
请确保：
1.进行全面的搜索来收集信息
2.验证信息的准确性
3.组织信息并撰写结构化的报告
"""

agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
    tools=[internet_search],
    system_prompt=SYSTEM_PROMPT,
)

query = "什么是资产减值？详细介绍一下它"

for event in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()
