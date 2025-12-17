"""
使用外部Postgresql实现会话的持久化
"""
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

DB_URI = "postgresql://postgres:123456@localhost:5432/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # 创建所需的数据表，仅需执行一次
    checkpointer.setup()

    agent = create_agent(
        model="openai:Qwen/Qwen3-8B",
        checkpointer=checkpointer,
    )

    config = {"configurable": {"thread": "1"}}

    results = agent.invoke({"messages": [{"role": "user", "content": "给我讲一首宋词"}]}, config=config)
    messages = results["messages"]
    for message in messages:
        message.pretty_print()

    results = agent.invoke({"messages": [{"role": "user", "content": "再来一首"}]}, config=config)
    messages = results["messages"]
    for message in messages:
        message.pretty_print()

    results = agent.invoke({"messages": [{"role": "user", "content": "再来一首看看呢"}]}, config=config)
    messages = results["messages"]
    for message in messages:
        message.pretty_print()
