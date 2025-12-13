import chromadb


# 列出向量库的collections和记录
def list_collection(db_path):
    client = chromadb.PersistentClient(db_path)
    collections = client.list_collections()
    print(f"chromadb:{db_path} 有 {len(collections)} 个 collection")
    for index, collection in enumerate(collections):
        print(f"collection - {index}: {collection.name}，共有 {collection.count()} 个记录")


# 删除向量库中的collection
def delete_collection(db_path, collection_name):
    try:
        client = chromadb.PersistentClient(db_path)
        client.delete_collection(collection_name)
    except Exception as e:
        print(f"删除 {collection_name} 失败，原因：{e}")


if __name__ == '__main__':
    db_path = "./chroma_langchain_db"
    list_collection(db_path)
