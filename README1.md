# 1. go to project
cd /Users/rohangupta/Desktop/LLM_Projects/LRAG-Chatbot

# 2. reset venv
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate

# 3. install deps
pip install --upgrade pip
pip install -r requirements.txt

# 4. start ollama (NEW TERMINAL)
ollama serve

# 5. ingest docs (NEW TERMINAL)
cd /Users/rohangupta/Desktop/LLM_Projects/LRAG-Chatbot
source venv/bin/activate
python ingest.py

# 6. start backend (NEW TERMINAL)
cd /Users/rohangupta/Desktop/LLM_Projects/LRAG-Chatbot
source venv/bin/activate
python app.py

# 7. test API
curl -X POST http://127.0.0.1:5000/ask \
-H "Content-Type: application/json" \
-d '{"question":"what is rag"}'

# 8. frontend (optional)
streamlit run streamlit.py
