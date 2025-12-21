"""
人在回路，human in the loop
- agent：集成大模型，集成工具，工具调用的时候，提供终端机制
- 人的确认：approval，reject，edit
- 中间件：middleware
"""
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()

# 系统提示词
SYSTEM_PROMT = """You are an expert weather forecaster, who speaks in puns.

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
    middleware=[
        # 人在回路
        HumanInTheLoopMiddleware(
            interrupt_on={
                "get_user_location": True,  # 所有决策都允许，approve，reject，edit
                "get_weather_for_location": {
                    "allowed_decision": ["approve", "reject"],
                }
            },
            description_prefix="工具执行挂起等待决策："
        )
    ],
    system_prompt=SYSTEM_PROMT,
)

# 配置thread_id
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面天气怎么样"}]},
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
for message in messages:
    message.pretty_print()

# dict，判断response是否有key: __interrupt__
if "__interrupt__" in response:
    print("INTERRUPTED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])

# 下发第一个指令
response = agent.invoke(
    Command(
        resume={"decisions": [
            {"type": "approve", }
        ]},
    ),
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
for message in messages:
    message.pretty_print()

# dict，判断response是否有key: __interrupt__
if "__interrupt__" in response:
    print("INTERRUPTED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])

# 下发第二个指令
response = agent.invoke(
    Command(
        resume={"decisions": [
            {"type": "approve", }
        ]},
    ),
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
for message in messages:
    message.pretty_print()

# dict，判断response是否有key: __interrupt__
if "__interrupt__" in response:
    print("INTERRUPTED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])
