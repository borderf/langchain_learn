"""
批量调用
"""
import asyncio
import time

from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
)

start = time.time()
inputs = [
    "翻译成英文：春天来了",
    "翻译成英文：夏天来了",
    "翻译成英文：秋天来了",
    "翻译成英文：冬天来了",
]

responses = model.batch(inputs)
batch_time = time.time() - start

for i, response in enumerate(responses):
    print(f"{i + 1}: {response.content}")

print(f"耗时：{batch_time:.2f}秒")

# 循环调用
start = time.time()
loop_responses = []
for input in inputs:
    reponse = model.invoke(input)
    loop_responses.append(response)
loop_time = time.time() - start
print(f"循环调用耗时：{loop_time:.2f}秒")


# 异步调用
async def translate_async(text: str) -> str:
    """异步翻译"""
    response = await model.ainvoke(f"翻译成英文：{text}")
    return response.content

async def main():
    """并发处理多个任务"""
    tasks = [
        translate_async("春天来了"),
        translate_async("夏天很热"),
        translate_async("秋天落叶"),
        translate_async("冬天下雪"),
    ]
    results = await asyncio.gather(*tasks)
    for i, result in enumerate(results):
        print(f"{i + 1}: {result}")

start = time.time()
asyncio.run(main())
async_time = time.time() - start
print(f"异步调用耗时：{async_time:.2f}秒")