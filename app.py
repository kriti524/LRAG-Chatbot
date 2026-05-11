from flask import Flask, request, jsonify
from llm import generate_answer, get_memory, clear
from ingest import ingest_local

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data     = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400
    answer, sources = generate_answer(question)
    return jsonify({"question": question, "answer": answer, "sources": sources})

@app.route("/ingest", methods=["POST"])
def ingest():
    ingest_local()
    return jsonify({"status": "ingested from docs/ folder"})

@app.route("/history", methods=["GET"])
def history():
    memory   = get_memory()
    messages = [{"role": m.type, "content": m.content}
                for m in memory.chat_memory.messages]
    return jsonify({"history": messages})

@app.route("/clear", methods=["POST"])
def clear_chat():
    clear()
    return jsonify({"status": "cleared"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)