from langchain.chat_models import init_chat_model
from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.5,

)

messages = [
    SystemMessage(content="你是一个专业的 Python 编程助手，擅长解释技术概念")
]
print("多轮对话（输入'quit'退出）")
while True:
    user_input = input("😄你：")
    if user_input == "quit":
        break
    # 保存用户信息
    messages.append(HumanMessage(content=user_input))

    # 调用模型
    response = model.invoke(messages)

    # 记录AI的回复
    messages.append(AIMessage(content=response.content))

    print(f"🤖 AI：{response.content}")