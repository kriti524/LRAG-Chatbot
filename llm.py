import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from rag import embeddings, CHROMA_DIR

load_dotenv()

_chain   = None
_memory  = None

def get_memory():
    global _memory
    if _memory is None:
        _memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    return _memory

def get_chain():
    global _chain
    if _chain is None:
        llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "llama2"),
            temperature=0.3
        )
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )
        prompt = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template="""You are a helpful assistant. Use the context to answer.
If unsure, say so honestly.

Chat history:
{chat_history}

Context:
{context}

Question: {question}
Answer:"""
        )
        _chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=get_memory(),
            combine_docs_chain_kwargs={"prompt": prompt},
            return_source_documents=True
        )
    return _chain

def generate_answer(question):
    chain  = get_chain()
    result = chain({"question": question})
    sources = list(set([
        doc.metadata.get("source", "unknown")
        for doc in result.get("source_documents", [])
    ]))
    return result["answer"], sources

def clear():
    global _chain, _memory
    _chain  = None
    _memory = None