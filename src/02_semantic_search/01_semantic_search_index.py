from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
"""
构建索引：从文本构建向量到存入到向量数据库
1、读取文本PDF，按照页来管理；
2、分割文本，将文本分割成文本块；
3、使用嵌入模型将文本块转化为向量；
4、将文本块向量存入到向量数据库；
"""
file_path = "D:\\文档\\阿里社区分享的用面试官的思维写简历.pdf"

# 1、读取PDF，按照页来管理，List[Document]
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))
print(f"{docs[1].page_content[:100]}")
print(docs[0].metadata)

# 2、分割文本，将文本分割为文本段（chunk），文本块也是List[Document]
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400, chunk_overlap=50, add_start_index=True
)

all_splits = text_splitter.split_documents(docs)

print(len(all_splits))
print(all_splits[0])

# 3、向量化：文本段 <=> 向量，使用嵌入模型辅助
from langchain_openai import OpenAIEmbeddings

embedding_model = OpenAIEmbeddings(
    model="BAAI/bge-m3"
)
# 向量的长度跟嵌入模型的维数有关
# vector_0 = embedding_model.embed_query(all_splits[0].page_content)
# print(vector_0)

# 4、文本块和向量的存储
from langchain_chroma import Chroma
vector_store = Chroma(
    # 存储的集合的名字
    collection_name="example_collection",
    # 声明转换使用的嵌入模型
    embedding_function=embedding_model,
    # 存储的位置，当前目录下
    persist_directory="./chroma_langchain_db"
)
# 将分割的文本块存入向量数据库，经过嵌入模型转化后存入
ids = vector_store.add_documents(all_splits)
print(ids)
