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
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location.
请用中文回答我
"""


@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# 工具运行时上下文传递参数
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


# 记忆管理
checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
    context_schema=Context,
    checkpointer=checkpointer,
    response_format=ToolStrategy(ResponseFormat),
    tools=[get_user_location, get_weather_for_location],
    system_prompt=SYSTEM_PROMPT,
)

# 配置thread_id
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面天气怎么样"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])

response = agent.invoke(
    {"messages": [{"role": "user", "content": "谢谢"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])
