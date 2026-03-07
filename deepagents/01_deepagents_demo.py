from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
)

agent = create_deep_agent(
    model=model,
)

while True:
    user_input = input("\n用户消息: ")
    if user_input.lower() in ["exit", "quit"]:
        print("结束对话")
        break
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })
    print("lallaal")
    for message in response["messages"]:
        message.pretty_print()