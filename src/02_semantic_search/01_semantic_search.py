from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = "D:\\文档\\阿里社区分享的用面试官的思维写简历.pdf"

loader = PyPDFLoader(file_path)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=50, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
print(len(docs))
print(f"{docs[1].page_content[:100]}")
print(docs[0].metadata)

print(len(all_splits))
