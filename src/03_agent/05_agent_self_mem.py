"""
使用自定义会话历史数组来实现记忆管理
"""
from langchain.agents import create_agent
from dotenv import load_dotenv
# 加载环境信息
load_dotenv()

agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
)

# 使用数组记录历史会话记录
his_messages = []
his_messages.append({"role": "user", "content": "来一首宋词"})
results = agent.invoke({"messages": his_messages})
messages = results["messages"]
for message in messages:
    message.pretty_print()

# 注意此时保存了之前的会话记录
his_messages.append({"role": "user", "content": "再来一首"})
results = agent.invoke({"messages": his_messages})
messages = results["messages"]
for message in messages:
    message.pretty_print()