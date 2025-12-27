"""
temperature：温度
0-2取值，越小越保守严谨，适合数学和代码的输出
越大越有创意开放，适合文学创作
"""
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

question = "请写一句关于春天的诗"

print("【保守模式】")

model1 = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    # 保守模式
    temperature=0.0,
)

for i in range(3):
    response = model1.invoke(question)
    print(f"第{i + 1}次：{response.content}")

print("*" * 50)

print("【创意模式】")
model2 = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    # 创意模式
    temperature=1
)
for i in range(3):
    response = model2.invoke(question)
    print(f"第{i + 1}次：{response.content}")
