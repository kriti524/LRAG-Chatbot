from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "./chroma_store"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

def add_documents(texts, ids):
    vectorstore.add_texts(texts=texts, ids=ids)
    print(f"Added {len(texts)} chunks to ChromaDB.")

def retrieve(query, top_k=3):
    results = vectorstore.similarity_search(query, k=top_k)
    return [r.page_content for r in results]