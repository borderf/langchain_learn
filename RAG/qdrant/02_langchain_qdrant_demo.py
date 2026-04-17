import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyMuPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import VectorParams, Distance

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

model_name = "Pro/MiniMaxAI/MiniMax-M2.5"
embedding_model_name = "BAAI/bge-m3"

load_dotenv()

logger.info("初始化模型...")
model = init_chat_model(
    model="Pro/MiniMaxAI/MiniMax-M2.5",
    model_provider="openai",
)
embeddings = OpenAIEmbeddings(model=embedding_model_name)
logger.info("模型初始化完成")

logger.info("初始化Qdrant客户端...")
client = QdrantClient(url="http://localhost:6333")
logger.info("Qdrant客户端连接成功")

docs = []
data_path = "D:\\docs\\ai\\财经学院"

logger.info("开始加载 PDF 文档...")
start_time = datetime.now()
pdf_loader = DirectoryLoader(
    path=data_path,
    glob="**/*.pdf",
    loader_cls=PyMuPDFLoader,
    show_progress=True,
)
pdf_docs = pdf_loader.load()
docs.extend(pdf_docs)
logger.info(f"PDF 加载完成: {len(pdf_docs)} 个文档，耗时 {datetime.now() - start_time}")

logger.info("开始加载 DOCX 文档...")
start_time = datetime.now()
docx_loader = DirectoryLoader(
    path=data_path,
    glob="**/*.docx",
    loader_cls=Docx2txtLoader,
    show_progress=True,
)
docx_docs = docx_loader.load()
docs.extend(docx_docs)
logger.info(f"DOCX 加载完成: {len(docx_docs)} 个文档，耗时 {datetime.now() - start_time}")

logger.info("开始加载 TXT 文档...")
start_time = datetime.now()
txt_loader = DirectoryLoader(
    path=data_path,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
    show_progress=True,
)
txt_docs = txt_loader.load()
docs.extend(txt_docs)
logger.info(f"TXT 加载完成: {len(txt_docs)} 个文档，耗时 {datetime.now() - start_time}")

logger.info(f"文档加载总计: {len(docs)} 个文档")

logger.info("开始分割文档...")
start_time = datetime.now()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
splits = text_splitter.split_documents(docs)
logger.info(f"文档分割完成，共 {len(splits)} 个片段，耗时 {datetime.now() - start_time}")

collection_name = "finance"
if not client.collection_exists(collection_name):
    logger.info(f"创建集合: {collection_name}")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            distance=Distance.COSINE,
            size=1024,
        )
    )
    logger.info("集合创建成功")
else:
    logger.info(f"集合 {collection_name} 已存在")

logger.info("开始向量化并存储到Qdrant...")
start_time = datetime.now()
vectorstore = QdrantVectorStore.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name=collection_name,
    url="http://localhost:6333",
)
logger.info(f"向量化存储完成，耗时 {datetime.now() - start_time}")

logger.info("全部完成！")
