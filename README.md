
# 🧠 SOP Chatbot Assistant

An AI-powered chatbot that helps users search and access Standard Operating Procedure (SOP) documents using natural language. Built with **Rasa**, **Streamlit**, and **ChromaDB**, this assistant performs semantic search over SOP documents and displays results in a chat-style UI.

---

## 🚀 Features

- 💬 Chat interface built with Streamlit
- 🧠 Semantic keyword extraction with spaCy
- 🔍 SOP document search via ChromaDB (vector store)
- 🤖 Rasa custom action integration
- 🔗 Clickable links to open matching SOP documents
- 🌐 Local file server to serve `.txt` files

---

## 📁 Project Structure

```
sop-chatbot/
│
├── chroma_db/
│   ├── db/
│   │   ├── chroma_client.py      # Initializes ChromaDB and SOP collection
│   │   └── sop_manager.py        # Loads and stores SOP chunks into ChromaDB
│   └── data/
│       └── sample_sops.json      # (optional) Sample input
│
├── rasa/
│   ├── actions/
│   │   └── actions.py            # Rasa custom action: action_search_sop
│   └── endpoints.yml             # Rasa action endpoint configuration
│
├── text_sop/                     # Folder containing SOP `.txt` files
│
├── streamlit_app.py              # Chat-style frontend with Streamlit
├── file_server.py                # Local file server for SOP files
├── requirements.txt              # Python dependencies
└── README.md                     # You're here
```

---

## 🛠️ Setup Instructions

### 1. 🐍 Create & Activate Virtual Environment

Make sure you have **Python 3.10+** installed.

```bash
python3 -m venv venv
```

Then activate it:

- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```
- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```

---

### 2. 📦 Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Also, install the spaCy language model:

```bash
python -m spacy download en_core_web_md
```

If `requirements.txt` is missing, you can regenerate it with:

```bash
pip freeze > requirements.txt
```

---

### 3. 📂 Prepare Your SOP Documents

Place your `.txt` SOP files into the `text_sop/` directory.  
Then, run the ingestion script to chunk and store them into ChromaDB:

```bash
python chroma_db/db/sop_manager.py
```

---

### 4. 🚀 Start the Services

#### 🧠 Rasa Custom Action Server

In one terminal:

```bash
rasa run actions
```

Make sure your `endpoints.yml` includes:

```yaml
action_endpoint:
  url: "http://localhost:5055/webhook"
```

#### 🌐 File Server (for SOP .txt files)

In another terminal:

```bash
python file_server.py
```

This serves files from `text_sop/` at:

```
http://localhost:8000/sop_documents/<filename>.txt
```

#### 💬 Streamlit Frontend

In a third terminal:

```bash
streamlit run streamlit_app.py
```

Go to: [http://localhost:8501](http://localhost:8501)

---

## 🧪 Example Flow

1. User types: `how to handle fire emergency`
2. Keywords extracted: `handle fire emergency`
3. ChromaDB returns top 3 SOP matches
4. Bot replies with clickable document links like:

```
I found these SOP documents:

[Open fire_emergency_procedure] 🔗
[Open safety_manual_section4] 🔗
```

Each opens the corresponding `.txt` file in a new tab.

---

## 📌 Notes

- You can customize the base document URL in `actions.py`:
  ```python
  DOCUMENT_BASE_URL = "http://localhost:8000/sop_documents/"
  ```
- ChromaDB persists in the `./chroma_db` directory.
- Streamlit uses `st.session_state` to maintain chat history.

---

## 💡 To Do

- [ ] Add user authentication
- [ ] PDF support with OCR (future)
- [ ] Deploy on cloud (e.g., AWS, GCP)
- [ ] Support document uploads via Streamlit

---

## 🧑‍💻 Author

**Satyam Kumar**  
🔗 Built with ❤️ using Python, Rasa, Streamlit, and ChromaDB

---
