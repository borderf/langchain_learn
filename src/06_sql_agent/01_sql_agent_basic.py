"""
SQL agent
"""
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from sympy.physics.units import temperature

load_dotenv()

model = init_chat_model(
    model="openai:Qwen/Qwen3-8B",
    temperature=0.1,
)

# todo next step
