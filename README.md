# AI RAG Chatbot with Memory

A Retrieval-Augmented Generation (RAG) chatbot that answers questions from uploaded documents using vector search and LLMs.

Built using LangChain, FAISS, HuggingFace embeddings, and Groq LLM.

---

## Features

• Chat with documents (PDF/TXT)
• Retrieval-Augmented Generation (RAG)
• FAISS vector database
• Conversation memory
• HuggingFace embeddings (free)
• Groq LLM integration (free)
• Streamlit web interface

---

## Tech Stack

Python
LangChain
FAISS
HuggingFace Embeddings
Groq LLM
Streamlit

---

## Project Structure

```
ai-rag-chatbot
│
├── app.py
├── requirements.txt
├── README.md
│
├── src
│   ├── chatbot.py
│   ├── config.py
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── memory.py
│   └── vector_store.py
│
├── data
│   ├── uploads
│   └── vector_store.faiss
│
└── tests
```

---

## Installation

Clone the repository:

```
git clone https://github.com/vextronlive/AI-RAG-chatbot.git
```

Go to project folder:

```
cd AI-RAG-chatbot
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the chatbot:

```
streamlit run app.py
```

---

## Example Workflow

1. Upload a document
2. The system splits it into chunks
3. Embeddings are created
4. Stored in FAISS vector database
5. When user asks a question → relevant chunks retrieved
6. LLM generates final answer

---

## Future Improvements

• Multi-document search
• Streaming responses
• Better UI
• Source citations
• Cloud deployment

---

## License

MIT License
