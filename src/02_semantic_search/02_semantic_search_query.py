from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

"""
向量数据库搜索
"""
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
# 查询1：相似度查询
results = vector_store.similarity_search(
    query="简历的编写技巧有哪些", k=2
)
for index, result in enumerate(results):
    print(index)
    print(result)

print("*" * 28)

# 查询2：带分数的相似度查询
results = vector_store.similarity_search_with_score(
    query="简历的编写技巧有哪些", k=2
)
for doc, score in results:
    print(doc)
    print(score)

print("=" * 28)
# 查询3：使用向量进行查询
embed_query = embedding_model.embed_query("简历的编写技巧有哪些")
results = vector_store.similarity_search_by_vector(embed_query)
for index, result in enumerate(results):
    print(index)
    print(result)
