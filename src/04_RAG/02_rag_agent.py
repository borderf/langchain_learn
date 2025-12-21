"""
RAG Agent
在agent的基础上如何做rag
"""
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool

load_dotenv()

# 新增嵌入模型和向量库
# 嵌入模型
embeddings = OpenAIEmbeddings(
    model="BAAI/bge-m3"
)
# 向量库
vector_store = Chroma(
    collection_name="rag_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_rag_db",
)


# 将检索的过程封装成工具
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query"""
    retrieve_docs = vector_store.similarity_search(query, k=2)
    content = "\n\n".join(
        (f"Source:{doc.metadata}\nContent:{doc.page_content}") for doc in retrieve_docs
    )
    return content, retrieve_docs


SYSTEM_FORMAT = """你可以使用信息检索工具，回答用户的问题"""

agent = create_agent(
    model="openai:Qwen/Qwen3-8B",
    tools=[retrieve_context],
    system_prompt=SYSTEM_FORMAT,
)

results = agent.invoke(
    {"messages": [{"role": "user", "content": "特朗普最近要做什么"}]}
)

messages = results["messages"]
for message in messages:
    message.pretty_print()
