"""
使用langchain的短期记忆管理-内存记忆管理
"""
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

# 检查点管理器，使用内存来实现
checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
    checkpointer=checkpointer,
)

# 检查点管理器是根据thread_id进行区分，后续对话需携带这个配置信息
config = {"configurable": {"thread_id": "1"}}

results = agent.invoke({"messages": [{"role": "user", "content": "来一首宋词"}]}, config=config)
messages = results["messages"]
for message in messages:
    message.pretty_print()

results = agent.invoke({"messages": [{"role": "user", "content": "再来一首"}]}, config=config)
messages = results["messages"]
for message in messages:
    message.pretty_print()
