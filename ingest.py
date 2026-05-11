import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag import add_documents

def ingest_local(folder="docs/"):
    loader = DirectoryLoader(folder, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)

    texts = [c.page_content for c in chunks]
    ids   = [f"doc_{i}" for i in range(len(chunks))]

    add_documents(texts, ids)
    print(f"✅ Ingested {len(chunks)} chunks from {len(docs)} files.")

if __name__ == "__main__":
    ingest_local()