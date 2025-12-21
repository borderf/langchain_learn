"""
rag索引
- 1.读取网页：获取文本，获取Document，List[Document]
- 2.分割文本：文本段（chunk），Document，List[Document]
- 3.向量化：文本段 => 向量，需要嵌入模型来辅助
- 4.向量库：把多个文本段/向量存到向量库
"""
import bs4
from langchain_chroma import Chroma
# 需要引入bs4，读取网页的工具
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

page_url = "https://www.163.com/news/article/KH9RBNRB000189FH.html"

bs4_strainer = bs4.SoupStrainer()

# 网页文档解析器
loader = WebBaseLoader(
    # 这个是一个元组
    web_paths=(page_url,),
    bs_kwargs={"parse_only": bs4_strainer},
)

docs = loader.load()

print(docs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)

all_splits = text_splitter.split_documents(docs)
print(len(all_splits))

embeddings = OpenAIEmbeddings(
    model="BAAI/bge-m3"
)

vector_store = Chroma(
    collection_name="rag_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_rag_db",
)

ids = vector_store.add_documents(documents=all_splits)

print(ids)
