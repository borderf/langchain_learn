from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    model="Qwen/Qwen3-8B",
    model_provider="openai",
    temperature=0.1,
    max_tokens=2000,
    timeout=None,
    max_retries=2,
)

for chunk in model.stream("来一段毛泽东的诗词"):
    print(chunk.content, end="", flush=True)
