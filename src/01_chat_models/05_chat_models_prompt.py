"""
方式一：直接使用字符串或字典；

方式二：系统提示词
系统提示词设计技巧：
1.明确角色：告诉AI是谁；
2.定义风格：正式/轻松，简洁/详细；
3.设定边界：什么能做，什么不能做；
4.输出格式：JSON、Markdown、纯文本；

few-shot：提示词中加入示例，输入和输出对应的示例
便于大模型按照设定的格式分析和输出
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
)

# 方式1：纯字符串（简单场景）
response = model.invoke("翻译成英文，你好世界")
print(response.content)

print("*" * 50)

# 方式2：消息列表（多轮对话）
messages = [
    {"role": "system", "content": "你是一个专业的翻译助手"},
    {"role": "user", "content": "翻译：Hello World"},
]

response = model.invoke(messages)
print(response.content)

print("*" * 50)

# 方式3：使用 Message 对象（兼容旧代码）
messages = [
    # 系统提示词，设置一次就可以了
    SystemMessage(content="你是一个专业的翻译助手"),
    HumanMessage(content="翻译：Hello World")
]

response = model.invoke(messages)
print(response.content)

print("*" * 50)

SYSTEM_PROMPT = """你是一个专业的 Python 编程助手。
    你的特点：
    - 擅长解释复杂概念
    - 代码示例清晰易懂
    - 注重最佳实践
    - 不使用已经废弃的语法
    
    回答要求：
    - 先解释原理，再给代码
    - 代码要有详细注释
    - 如果有多种方案，说明优劣
"""
messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content="什么是装饰器"),
]
response = model.invoke(messages)
print(response.content)

print("*" * 50)


FEW_SHOT_PROMPT = """你是一个情感分析助手。根据文本判断情感倾向。
示例1：
输入：今天天气真好，心情很愉快！
输出：正面 | 置信度：0.95

示例2：
输入：产品质量太差了，非常失望。
输出：负面 | 置信度：0.90

示例3：
输入：今天去了超市买东西
输出：中性 | 置信度：0.85

现在分析下面的文本：
"""
user_input = "这个课程很实用，学到了很多！"

messages = [
    SystemMessage(content=FEW_SHOT_PROMPT),
    HumanMessage(content=user_input),
]

response = model.invoke(messages)
print(response.content)

print("*" * 50)


"""
提示词模板示例
"""
class PromptTemplate:
    """简单的提示词模板类"""
    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs):
        return self.template.format(**kwargs)

# 定义模板
translation_template = PromptTemplate(
    """你是一个专业的翻译助手。
    任务：将 {source_lang} 翻译成 {target_lang}
    风格：{style}
    原文：
    {text}
    翻译："""
)

# 使用模板
prompt = translation_template.format(
    source_lang="中文",
    target_lang="英文",
    style="正式",
    text="人工智能正在改变世界"
)

response = model.invoke(prompt)
print(response.content)