"""
默认的方式是l2
cosine：两个向量的夹角度量相似度 1-cos(角度)
    - cosine value returns cosine distance rather then cosine similarity. Ie. values close to 0 means the embeddings are more similar
l2：两个向量的距离度量相似度
ip：两个向量的内积/点积度量相似度，和cosine接近
"""
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 定义嵌入模型
embeddings = OpenAIEmbeddings(model="BAAI/bge-m3")

# 评分标准
score_measures = [
    "default",  # 默认度量相似度方式
    "cosine",  # 两个向量夹角度量相似度
    "l2",  # 两个向量的距离度量相似度
    "ip"  # 两个向量的内积/点积度量相似度
]

# 创建向量库和4个collection
persist_dir = "./chroma_score_db"
vector_stores = []
for score_measure in score_measures:
    collection_metadata = {"hnsw:space": score_measure}
    if score_measure == "default":
        collection_metadata = None
    collection_name = f"my_collection_{score_measure}"
    vector_store = Chroma(
        collection_name=collection_name,
        collection_metadata=collection_metadata,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
    vector_stores.append(vector_store)


# 创建索引
def indexing(docs):
    print("创建索引，加入文档")
    for vector_store in vector_stores:
        ids = vector_store.add_documents(docs)
        print(f"集合：{vector_store._collection.name}")
        print(ids)


def query_with_score(query: str):
    for i in range(len(score_measures)):
        results = vector_stores[i].similarity_search_with_score(query)
        print(f"搜索：{query}")
        for doc, score in results:
            print(doc.page_content)
            print(f"{score_measures[i]}: {score}")
        print("*" * 28)


if __name__ == '__main__':
    # 创建索引的过程
    # docs = [
    #     Document("这个小米手机很好用"),
    #     Document("我国陕北地区盛产小米")
    # ]
    # indexing(docs)
    query_with_score("小米手机怎么样")
