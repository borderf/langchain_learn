"""
智能翻译助手
"""
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage


class SmartTranslator:
    def __init__(self):
        self.model = model = init_chat_model(
            model="Qwen/Qwen3-8B",
            model_provider="openai",
            temperature=0.3,
        )

    def translate(self, text: str, target_language: str = "中文", style: str = "正式"):
        """
        翻译文本
        :param text:    要翻译的文本
        :param target_language: 目标语言（中文/英文/日文等）
        :param style:   翻译风格（正式/口语/文学等）
        """
        SYSTEM_PROMPT = f"""
            你是一个专业的翻译助手。
            任务：
            1.自动检测输入文本的语言；
            2.翻译成{target_language}
            3.使用{style}风格
            4.如果有专业术语，在翻译后用括号标注原文
            
            输出格式：
            【源语言】：xxx
            【翻译】：xxx
            【术语解释】：（如果有）
        """
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=text),
        ]

        response = self.model.invoke(messages)
        return response.content


if __name__ == '__main__':
    translator = SmartTranslator()
    print("🤖智能翻译助手")
    print("*" * 50)
    text1 = "Langchain is a framework for developing applications powered by large language models."
    print(f"📝原文：{text1}")
    print(f"📝翻译结果：{translator.translate(text1, "中文", "正式")}")
