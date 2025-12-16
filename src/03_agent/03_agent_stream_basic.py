"""
agent的流式输出
"""
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


def get_weather(city: str):
    """获取给定城市的天气"""
    return f"{city}最近的天气相当好，适合出去玩哦"


agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
    tools=[get_weather]
)

# stream_output = agent.stream({"messages": [{"role": "user", "content": "成都最近的天气怎么样"}]}, stream_mode="values")
# for chunk in stream_output:
#     # 只显示最新的一条消息
#     latest_message = chunk["messages"][-1]
#     latest_message.pretty_print()

stream_output = agent.stream({"messages": [{"role": "user", "content": "成都最近的天气怎么样"}]}, stream_mode="messages")
for token, metadata in stream_output:
    # token by token
    # print(f"node: {metadata['langgraph_node']}")
    # print(f"content: {token.content}")
    # print()
    # 连续打印
    print(token.content, end="")
