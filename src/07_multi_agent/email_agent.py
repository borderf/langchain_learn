"""
email agent
"""
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# 模型
model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
)

EMAIL_AGENT_PROMPT = (
    "You are an email assistant. "
    "Compose professional emails based on natural language requests. "
    "Extract recipient information and craft appropriate subject lines and body text. "
    "Use send_email to send the message. "
    "Always confirm what was sent in your final response."
)


@tool
def send_email(
    to: list[str], subject: str, body: str, cc: list[str] = []  # email addresses
) -> str:
    """Send an email via email API. Requires properly formatted addresses."""
    # Stub: In practice, this would call SendGrid, Gmail API, etc.
    return f"Email sent to {', '.join(to)} - Subject: {subject}"

email_agent = create_agent(
    model,
    tools=[send_email],
    system_prompt=EMAIL_AGENT_PROMPT,
)


query = "Send the design team a reminder about reviewing the new mockups"

for step in email_agent.stream({"messages": [{"role": "user", "content": query}]}):
    for update in step.values():
        for message in update.get("messages", []):
            message.pretty_print()
