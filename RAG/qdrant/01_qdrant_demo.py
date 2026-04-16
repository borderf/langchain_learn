from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

# 创建集合（先检查是否存在）
collection_name = "test_collection"

# 检查集合是否存在
collections = client.get_collections().collections
exists = any(c.name == collection_name for c in collections)

if not exists:
    print(f"创建集合: {collection_name}")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=128,  # 这里改成你的 embedding 维度
            distance=models.Distance.COSINE
        )
    )
else:
    print(f"集合 {collection_name} 已存在，跳过创建")

# client.upsert(
#     collection_name="test_collection",
#     points=[
#         models.PointStruct(
#             id=1,  # Qdrant 要求 ID 为整数或 UUID
#             vector=[0.1] * 128,
#             payload={
#                 "kb_id": "hr_policy",
#                 "doc_id": "DOC-001",
#                 "doc_title": "员工请假制度",
#                 "doc_type": "policy",
#                 "department_code": "HR",
#                 "version": "v3",
#                 "acl_roles": ["employee", "manager"],
#                 "chunk_no": 1,
#                 "text": "连续请假超过3天,需直属主管审批。"
#             }
#         )
#     ]
# )

def search_without_filter(client: QdrantClient):
    query_vector = [0.1] * 128
    hits = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=5
    )

    print("\n=== search_without_filter ===")
    for hit in hits.points:
        print(
            f"id={hit.id}, score={hit.score:.4f}, "
            f"title={hit.payload.get('doc_title')}, "
            f"text={hit.payload.get('text')}"
        )

# search_without_filter(client)

def search_with_filter(client: QdrantClient):
    query_vector = [0.1] * 128
    hits = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=5,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="department_code",
                    match=models.MatchValue(value="HR")
                )
            ]
        )
    )

    print("\n=== search_with_filter ===")
    for hit in hits.points:
        print(
            f"id={hit.id}, score={hit.score:.4f}, "
            f"title={hit.payload.get('doc_title')}, "
            f"text={hit.payload.get('text')}"
        )

search_with_filter(client)


