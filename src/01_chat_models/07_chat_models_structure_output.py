"""
模型的结构化输出
"""
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model


# 定义输出结构
class SentimentAnalysis(BaseModel):
    """情感分析结果"""
    sentiment: str = Field(description="情感倾向：positive/negative/neutral")
    confidence: float = Field(description="置信度，0-1之间")
    keywords: list[str] = Field(description="关键词列表")


model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
)

# 给模型设定结构化输出
structured_model = model.with_structured_output(SentimentAnalysis)

text = "这个课程很实用，学到了很多知识，强烈推荐"

result = structured_model.invoke(
    f"分析以下文本的情感：\n{text}"
)

print(f"类型：f{type(result)}")
print(f"情感：{result.sentiment}")
print(f"置信度：{result.confidence}")
print(f"关键词：{result.keywords}")

print("*" * 50)

"""
复杂的结构化输出
"""


class Aspect(BaseModel):
    """评论维度"""
    name: str = Field(description="维度名称，如：质量、价格、服务等")
    score: int = Field(description="评分：1-5")
    comment: str = Field(description="具体评价")


class ProductReview(BaseModel):
    """产品评论分析"""
    overall_sentiment: str = Field(description="整体情感：positive/negative/neutral")
    overall_score: int = Field(description="综合评分：1-5")
    aspects: list[Aspect] = Field(description="各维度评价")
    summary: str = Field(description="一句话总结")


# 创建结构化模型
structured_model = model.with_structured_output(ProductReview)
# 测试
review_text = """
这款笔记本非常强大，运行大型软件毫无压力。
屏幕色彩鲜艳，看视频很舒服。
不过价格有点贵，而且风扇噪音较大。
客服态度很好，物流速度也很快。
总体来说还是很值得购买。
"""

result = structured_model.invoke(
    f"分析以下产品评论：\n{review_text}"
)

print(result)
