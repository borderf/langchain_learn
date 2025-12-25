from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
)

messages = [
    SystemMessage(content="你是一个商业分析专家"),
]

print("开始进行多轮对话，输入'quit'退出")
while True:
    user_input = input("😄你：")
    if user_input == "quit":
        break

    messages.append(HumanMessage(content=user_input))

    response = model.stream(messages)

    print("🤖AI：", end="")

    ai_message_content = ""
    for message in response:
        ai_message_content += message.content
        print(message.content, end="", flush=True)

    messages.append(AIMessage(content=ai_message_content))

    print()
