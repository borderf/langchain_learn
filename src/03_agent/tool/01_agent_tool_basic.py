"""
agent的工具调用
"""
import math
from datetime import datetime

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from pyexpat.errors import messages


@tool
def calculator(expression: str) -> str:
    """
    计算数学表达式：
    支持基本运算：+、-、*、/、**（幂）、sqrt（平方根）
    Args：expression：数学表达式字符串，如"2+3*4"或"sqrt(16)"
    Returns: 计算结果
    Examples：calculator("10+5") 返回 "15.0"
    """
    try:
        safe_dict = {
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs,
        }
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return str(result)
    except Exception as error:
        print(f"计算错误：{error}")


@tool
def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取当前时间
        Args：timezone：时区，默认"Asia/Shanghai"（北京时间）
        Returns: 格式化当前时间字符串
    """
    now = datetime.now()
    return now.strftime(timezone)


@tool
def search_product(keyword: str) -> str:
    """
    商品搜索
    :param keyword: 关键词
    :return: 产品列表（模拟数据）
    """
    products = {
        "手机": "iPhone 17:￥5999,小米17:￥4999,华为Mate80:￥4999",
        "笔记本": "Macbook Pro:￥12999,ThinkPad X1:￥9999,华为MateBook:￥10999",
        "耳机": "AirPods Pro:￥1999,Sony WH-1000XM6:￥2499,小米降噪耳机:￥799"
    }
    for key, value in products.items():
        if keyword in key:
            return f"找到相关产品\n{value}"

    return f"未找到关于{keyword}的产品"


model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
)

agent = create_agent(
    model=model,
    tools=[get_current_time, search_product],
    debug=True, # 调试模式
    system_prompt="你是一个有用的助手"
)

result = agent.invoke({"messages": [{"role": "user", "content": "现在是几点了，然后帮我找一下手机的商品信息"}]})
messages = result["messages"]
print(messages[-1].content)
