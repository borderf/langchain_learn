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

from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# 系统提示词
SYSTEM_PROMT = """你是一个专业的天气预报专家，请以诙谐的语气回答我
你可以使用两个工具:
- get_weather_for_location: 使用这个去获取特定地址的天气
- get_user_location: 使用这个去获取用户的地址
当用户询问你天气的时候，确保你知道用户的地址，如果你能判断出用户的地址，使用get_user_location去获取他的地址
请用中文回答我
"""


@tool
def get_weather_for_location(location: str) -> str:
    """获取一个给定地址的天气"""
    return f"{location}永远都是好天气！"


# 工具运行时上下文传递参数
@dataclass
class Context:
    """自定义运行时上下文"""
    user_id: str


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户的ID检索用户信息"""
    user_id = runtime.context.user_id
    return "杭州" if user_id == "1" else "成都"


@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_condition: str | None = None


# 记忆管理
checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
    context_schema=Context,
    checkpointer=checkpointer,
    response_format=ToolStrategy(ResponseFormat),
    tools=[get_user_location, get_weather_for_location],
    system_prompt=SYSTEM_PROMT,
)

# 配置thread_id
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke({"messages": [{"role": "user", "content": "外面的天气怎么样？"}]},
                        config=config,
                        context=Context(user_id="1"))
print(response["structured_response"])

response = agent.invoke({"messages": [{"role": "user", "content": "谢谢"}]},
                        config=config,
                        context=Context(user_id="1"))
print(response["structured_response"])
