# LRAG-Chatbot
A local Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Ollama, ChromaDB, Flask, and Streamlit. Supports document ingestion, semantic search, conversational memory, and source-aware AI responses using local LLMs.

# Local RAG Chat Assistant

A Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Ollama, ChromaDB, Flask, and Streamlit.

The system allows users to ingest local documents and chat with them using a local LLM powered by semantic search and conversational memory.

---

# Features

* Local document ingestion from `docs/`
* Semantic search using vector embeddings
* Conversational memory support
* Source-aware responses
* Local LLM inference via Ollama
* Persistent vector storage with ChromaDB
* Streamlit-based chat interface

---

# Project Structure

```bash id="r8x2pd"
project/
│
├── app.py
├── ingest.py
├── llm.py
├── rag.py
├── streamlit.py
├── requirements.txt
├── docs/
├── README.md
├── Screenshot_1.png
├── Screenshot_2.png
```

---

# Installation

## Clone Repository

```bash id="n2k7qa"
git clone https://github.com/your-username/local-rag-chat.git
cd local-rag-chat
```

---

## Create Virtual Environment

### Windows

```bash id="c5m9vx"
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash id="t1p6sd"
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash id="k7z3mw"
pip install -r requirements.txt
```

---

# Install and Run Ollama

Download Ollama:

```text id="v4j8qn"
https://ollama.com/download
```

Pull a model:

```bash id="h9s2ld"
ollama pull llama2
```

Start Ollama server:

```bash id="p6w1zx"
ollama serve
```

---

# Environment Variables

Create a `.env` file:

```env id="q8n4tc"
OLLAMA_MODEL=llama2
FLASK_API_URL=http://localhost:5001
```

---

# Add Documents

Place `.txt` files inside the `docs/` folder.

Example:

```bash id="d3k7ra"
docs/
├── notes.txt
├── research.txt
├── company_docs.txt
```

---

# Run the Application

## Start Flask Backend

```bash id="z6x2mv"
python app.py
```

---

## Start Streamlit Frontend

```bash id="u8p5sc"
streamlit run streamlit.py
```

---

# Workflow

```text id="l9c1wx"
Documents (docs/)
   ↓
Chunking (ingest.py)
   ↓
Embeddings (rag.py)
   ↓
ChromaDB Storage
   ↓
Retriever (llm.py)
   ↓
LangChain RAG Chain
   ↓
Ollama LLM
   ↓
Response + Sources
   ↓
Streamlit UI
```

---

# Notes

* Ensure Ollama is running before starting the backend
* Run ingestion before asking questions
* Only `.txt` files are supported inside `docs/`

---

