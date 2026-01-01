"""
supervisor agent
"""

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

from calendar_agent_HITL import calendar_agent
from email_agent_HITL import email_agent


load_dotenv()

# 模型
model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
)


@tool
def schedule_event(request: str) -> str:
    """Schedule calendar events using natural language.

    Use this when the user wants to create, modify, or check calendar appointments.
    Handles date/time parsing, availability checking, and event creation.

    Input: Natural language scheduling request (e.g., 'meeting with design team
    next Tuesday at 2pm')
    """
    result = calendar_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text


@tool
def manage_email(request: str) -> str:
    """Send emails using natural language.

    Use this when the user wants to send notifications, reminders, or any email
    communication. Handles recipient extraction, subject generation, and email
    composition.

    Input: Natural language email request (e.g., 'send them a reminder about
    the meeting')
    """
    result = email_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text


SUPERVISOR_PROMPT = (
    "You are a helpful personal assistant. "
    "You can schedule calendar events and send emails. "
    "Break down user requests into appropriate tool calls and coordinate the results. "
    "When a request involves multiple actions, use multiple tools in sequence."
)


supervisor_agent = create_agent(
    model,
    tools=[schedule_event, manage_email],
    system_prompt=SUPERVISOR_PROMPT,
    checkpointer=InMemorySaver(),
)


query = "Schedule a meeting with the design team on 2026/1/1 at 2:00pm for 1 hour, and send Alice,Bob,Cindy an email reminder about reviewing the new mockups."

config = {"configurable": {"thread_id": "6"}}

interrupts = []
for step in supervisor_agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    config,
):
    for update in step.values():
        if isinstance(update, dict):
            for message in update["messages"]:
                message.pretty_print()

        else:
            interrupt = update[0]
            interrupts.append(interrupt)
            # print(f"\nINTERRUPTED: {interrupt.id}")

for interrupt_ in interrupts:
    for request in interrupt_.value["action_requests"]:
        print(f"INTERRUPTED: {interrupt_.id}")
        print(f"{request['description']}\n")
