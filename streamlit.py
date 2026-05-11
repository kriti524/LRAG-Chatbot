import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("FLASK_API_URL", "http://localhost:5001")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RAG Chat",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to bottom right, #0b0f1a, #151124);
    color: #f3f4f6;
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1e1b35);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Main Title */
.main-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #5b8cff, #ff5ec4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}

/* Subtitle */
.sub-title {
    color: #9ca3af;
    margin-top: -10px;
    margin-bottom: 25px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    background: linear-gradient(90deg, #5b8cff, #ff5ec4);
    color: white;
    font-weight: 600;
    padding: 10px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.02);
    opacity: 0.92;
}

/* Chat Input */
.stChatInput input {
    background-color: #1f2937 !important;
    color: white !important;
    border: 1px solid #374151 !important;
    border-radius: 16px !important;
    padding: 14px !important;
}

/* User Message */
.user-message {
    background: linear-gradient(135deg, #5b8cff, #7f5cff);
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 12px 0;
    box-shadow: 0 4px 15px rgba(91,140,255,0.25);
}

/* Assistant Message */
.assistant-message {
    background: rgba(31,41,55,0.85);
    color: #f3f4f6;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 12px 0;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
}

/* Source Box */
.source-box {
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #ff5ec4;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
    color: #d1d5db;
}

/* Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.05);
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    text-align: center;
    backdrop-filter: blur(8px);
}

.metric-title {
    color: #9ca3af;
    font-size: 14px;
}

.metric-value {
    color: white;
    font-size: 16px;
    font-weight: 600;
    margin-top: 4px;
}

/* Expander */
.streamlit-expanderHeader {
    color: #f3f4f6 !important;
    font-weight: 600;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 10px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">Chat Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">LangChain · Ollama · ChromaDB · Flask · Streamlit</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("Controls")

    if st.button("Ingest Documents"):
        with st.spinner("Processing documents..."):
            res = requests.post(f"{API}/ingest")
            st.success(res.json().get("status"))

    if st.button("Clear History"):
        requests.post(f"{API}/clear")
        st.session_state.messages = []
        st.success("Conversation cleared")

    st.divider()

    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-title">Model</div>
        <div class="metric-value">
            {os.getenv("OLLAMA_MODEL", "llama2")}
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="metric-card">
        <div class="metric-title">Vector Database</div>
        <div class="metric-value">ChromaDB</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="metric-card">
        <div class="metric-title">Embeddings</div>
        <div class="metric-value">MiniLM-L6-v2</div>
    </div>
    ''', unsafe_allow_html=True)

# ---------------- CHAT STORAGE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:

    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-message">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f'<div class="assistant-message">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(
                        f'<div class="source-box">{s}</div>',
                        unsafe_allow_html=True
                    )

# ---------------- CHAT INPUT ----------------
if question := st.chat_input("Ask about your documents..."):

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.markdown(
        f'<div class="user-message">{question}</div>',
        unsafe_allow_html=True
    )

    # ASSISTANT RESPONSE
    with st.spinner("Generating response..."):

        try:
            res = requests.post(
                f"{API}/ask",
                json={"question": question}
            )

            data = res.json()

            answer = data.get(
                "answer",
                "Something went wrong."
            )

            sources = data.get("sources", [])

        except Exception as e:
            answer = f"Error: {str(e)}"
            sources = []

    st.markdown(
        f'<div class="assistant-message">{answer}</div>',
        unsafe_allow_html=True
    )

    if sources:
        with st.expander("Sources"):
            for s in sources:
                st.markdown(
                    f'<div class="source-box">{s}</div>',
                    unsafe_allow_html=True
                )

    # SAVE CHAT
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })