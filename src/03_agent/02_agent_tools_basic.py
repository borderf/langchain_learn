"""
简单的工具调用
"""
from langchain.agents import create_agent
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# 定义工具函数
# 注意定义工具函数，必须要有文档说明，给大模型说明这个工具函数是干什么的
def get_weather(city: str):
    """获取给定城市的天气"""
    return f"{city}最近的天气相当好，适合出去玩哦"


agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
    tools=[get_weather]
)

print(agent)
# {'__start__': <langgraph.pregel._read.PregelNode object at 0x0000021ADC3CEB70>,
#   'model': <langgraph.pregel._read.PregelNode object at 0x0000021ADC436960>,
#   'tools': <langgraph.pregel._read.PregelNode object at 0x0000021ADC17B8C0>}
print(agent.nodes)

results = agent.invoke({"messages": {"role": "user", "content": "成都最近的天气怎么样"}})
# ================================ Human Message =================================
#
# 成都最近的天气怎么样
# ================================== Ai Message ==================================
# Tool Calls:
#   get_weather (019b2796ccb6c232c0eb30518720afd1)
#  Call ID: 019b2796ccb6c232c0eb30518720afd1
#   Args:
#     city: 成都
# ================================= Tool Message =================================
# Name: get_weather
#
# 成都最近的天气相当好，适合出去玩哦
# ================================== Ai Message ==================================
#
# 成都最近的天气相当好，适合出去玩哦！如果您有具体的出行计划或需要更多天气详情，可以随时告诉我，我会为您提供更详细的帮助。
messages = results["messages"]
for message in messages:
    message.pretty_print()
