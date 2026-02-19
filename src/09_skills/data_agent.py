"""
Deep Agents 使用 Skills 的简单示例

Skills 是一种基于提示词的专项能力封装，通过渐进式披露（progressive disclosure）
让 Agent 按需加载所需的技能知识，而不是一次性加载所有内容。

本示例包含两个技能：
- greeting: 问候打招呼
- joke: 讲笑话
"""

from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from deepagents import create_deep_agent

load_dotenv()

SKILLS_DIR = Path(__file__).parent / "skills"

SYSTEM_PROMPT = """你是一个友好的聊天助手。

你可以：
- 和用户打招呼聊天
- 给用户讲笑话

请根据用户的需求选择合适的技能来回应。
"""


def create_chat_agent():
    model = init_chat_model(
        model="Qwen/Qwen3-8B",
        model_provider="openai",
        temperature=0.7,
    )

    agent = create_deep_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        skills=[str(SKILLS_DIR)],
        checkpointer=InMemorySaver(),
    )

    return agent


def main():
    agent = create_chat_agent()

    print("=" * 50)
    print("聊天助手已启动（输入 'exit' 退出）")
    print("试试说：你好 / 给我讲个笑话")
    print("=" * 50)

    thread_id = "chat_session_001"
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        user_input = input("\n用户: ").strip()
        if user_input.lower() == "exit":
            print("再见！")
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
        )

        for message in result["messages"]:
            if hasattr(message, "pretty_print"):
                message.pretty_print()


if __name__ == "__main__":
    main()
