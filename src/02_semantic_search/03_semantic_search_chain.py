"""
语义搜索用chain连接
"""
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# 嵌入模型
embedding_model = OpenAIEmbeddings(
    model="BAAI/bge-m3"
)
# 向量数据库
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embedding_model,
    persist_directory="./chroma_langchain_db"
)

# 将语义查询封装成chain上的一个节点，定义为Runnable
@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)


results = retriever.invoke("简历的编写技巧有哪些")
for index, result in enumerate(results):
    print(index)
    print(result)
