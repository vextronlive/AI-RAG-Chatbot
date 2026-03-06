# 🤖 AI Chatbot with Memory (RAG-based)

> A semester project built for my 4th semester Machine Learning course.
> 
> **Status:** ✅ Complete and working  
> **Time to build:** ~2 weeks  
> **Cost:** **$0 (Completely FREE!)** 💰  
> **Lines of code:** ~1,300

---

## 💰 FREE API Options (No Payment Required!)

This project supports **completely FREE** APIs:

| Provider | Cost | Speed | Setup | Best For |
|----------|------|-------|-------|----------|
| **Groq** | FREE (1M tokens/day) | ⚡ Very Fast | Easy | Beginners |
| **Ollama** | 100% FREE | 🐢 Slower | Medium | Privacy/Offline |

**Recommended for students:** Use **Groq** - it's free, fast, and takes 2 minutes to set up!

---

## 📋 What is this?

An AI chatbot that can:
- **Answer questions** based on PDF documents you upload
- **Remember conversation history** (follow-up questions work!)
- **Cite sources** (tells you which page the info came from)
- **Run for FREE** using Groq or Ollama

Built using **RAG (Retrieval-Augmented Generation)** - the chatbot "looks up" relevant info before answering.

---

## 🚀 Quick Start (FREE Setup - 5 Minutes!)

### Step 1: Get Your FREE Groq API Key

1. Go to **[console.groq.com](https://console.groq.com/keys)**
2. Sign up (free, just email/GitHub)
3. Click "Create API Key"
4. Copy your key (starts with `gsk_`)

> 💡 **Free tier:** 1,000,000 tokens per day (more than enough!)

### Step 2: Download & Setup Project

```bash
# Download the project
cd ai_chatbot_memory

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Groq key:
# GROQ_API_KEY=gsk_your_key_here
```

### Step 4: Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 🖥️ Alternative: 100% FREE with Ollama (Local)

Want to run everything on your computer with **zero internet** (after setup)?

### Setup Ollama (One-time)

```bash
# 1. Download Ollama from https://ollama.com/download

# 2. Pull a model (~2GB download)
ollama pull llama3.2

# 3. Start the server
ollama serve
```

### Configure Project

Edit `.env`:
```
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=huggingface
# No API key needed!
```

### Run

```bash
streamlit run app.py
```

✅ **Completely free forever!** No API calls, no limits, fully private.

---

## 📁 Folder Structure

```
ai_chatbot_memory/
│
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
├── .env.example             # API configuration template
├── README.md                # This file
│
├── src/                     # Core modules
│   ├── config.py           # Settings (supports FREE APIs!)
│   ├── document_processor.py # PDF processing
│   ├── embeddings.py        # FREE HuggingFace embeddings
│   ├── vector_store.py      # FAISS database
│   ├── memory.py            # Conversation history
│   └── chatbot.py           # RAG engine (Groq/Ollama/OpenAI)
│
├── data/                    # Data storage
│   ├── uploads/            # Uploaded PDFs
│   └── sample_report.py    # Create test PDF
│
└── tests/                   # Test files
    └── test_chatbot.py
```

---

## 📖 How to Use

### 1. Upload a PDF

- Use the sidebar to upload a PDF
- Click "Process PDF"
- Wait for success message

### 2. Ask Questions

Type in the chat box:
- "What is this document about?"
- "Summarize the main points"
- "What does the author say about [topic]?"

### 3. Follow-up Questions Work!

```
You: "What is machine learning?"
Bot: "Machine learning is..."

You: "What are its types?"  ← Bot remembers "its" = ML!
Bot: "The types are..."
```

### 4. View Sources

Click "📎 Sources" to see which pages the answer came from.

---

## 🔬 How It Works

### 1. Embeddings (Text → Numbers)

```
"The cat sat on the mat"     → [0.23, -0.45, 0.89, ...]
"A feline rested on the rug" → [0.25, -0.42, 0.87, ...]
# Similar meaning = similar vectors!
```

**We use FREE HuggingFace embeddings** - no API key needed!

### 2. FAISS (Fast Search)

- Stores embedding vectors
- Finds similar ones quickly
- Completely free and open source

### 3. RAG Flow

```
Question → Embed → Search FAISS → Get Chunks → Build Prompt → LLM → Answer
```

### 4. Memory

Stores conversation history so follow-up questions work correctly.

---

## 💰 Cost Comparison

| Component | Our Choice | Cost |
|-----------|-----------|------|
| **LLM** | Groq (Free tier) | **$0** |
| **Embeddings** | HuggingFace | **$0** |
| **Vector DB** | FAISS | **$0** |
| **Total** | | **$0** ✅ |

**With OpenAI (for comparison):**
- GPT-3.5: ~$0.002 per 1K tokens
- Embeddings: ~$0.0001 per 1K tokens
- Typical use: $1-5 per project

---

## 🧪 Testing

### Create Sample PDF

```bash
python data/sample_report.py
```

### Run Tests

```bash
python tests/test_chatbot.py
```

### Sample Questions (for testing)

Upload the sample PDF and try:

1. **"What is machine learning?"**
2. **"What are the types of ML?"**
3. **"Give me examples"** (tests memory!)
4. **"Summarize the document"**

---

## 🎓 Viva Questions

### Q1: What is RAG?

**A:** Retrieval-Augmented Generation. We:
1. Retrieve relevant documents using vector search
2. Add them to the LLM prompt as context
3. Generate answer based on that context

**Benefits:** Reduces hallucination, uses custom data, provides citations.

### Q2: Why use Groq instead of OpenAI?

**A:** 
- **Groq is FREE** (1M tokens/day)
- **Extremely fast** inference (fastest available)
- Uses same quality models (Llama 3, Mixtral)
- Perfect for student projects and learning

### Q3: How do embeddings work?

**A:** Embeddings convert text to vectors that capture meaning. Similar texts have similar vectors. We use **HuggingFace's free model** that runs locally on CPU.

### Q4: Why FAISS?

**A:** FAISS is a free, open-source library for fast similarity search. It finds similar vectors in O(log n) time instead of O(n).

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "GROQ_API_KEY not found" | Get free key from [console.groq.com](https://console.groq.com/keys) |
| "Model not found" (Ollama) | Run `ollama pull llama3.2` |
| "Connection refused" (Ollama) | Run `ollama serve` in another terminal |
| Slow first run | HuggingFace downloads model (~80MB) - one time only |
| Out of memory | Use smaller model: `llama3-8b-8192` instead of `llama3-70b-8192` |

---

## 🔮 Future Improvements

Realistic enhancements:

1. **More file formats:** Word, TXT, Markdown
2. **Persistent chat history:** Save to SQLite
3. **Better chunking:** Semantic splitting
4. **Export chats:** Save as PDF/text
5. **Multiple LLM support:** Switch between providers in UI

---

## 📚 What I Learned

- **RAG architecture** - Combining retrieval + generation
- **Vector embeddings** - Converting meaning to math
- **FAISS** - Fast similarity search
- **Free LLM APIs** - Groq, Ollama
- **LangChain** - Modular LLM framework
- **Streamlit** - Easy web UIs

---

## 🙏 Acknowledgments

- **Groq** - For the generous free tier
- **HuggingFace** - For free embeddings
- **LangChain** - For the framework
- **FAISS** - For vector search
- **Ollama** - For local LLMs

---

## 📄 License

Student project - free to use for learning!

---

**Built with ❤️ for my 4th semester ML course.**

*Last updated: March 2025*
��──────┘
      │
      ▼
┌─────────────┐
│  Send to    │  ← LLM generates answer
│    LLM      │
└─────────────┘
```

**Code:** `src/chatbot.py`

### 4. Memory - Remembering Context

**Why memory matters:**

Without memory:
```
User: "My name is Alice"
Bot: "Nice to meet you!"
User: "What's my name?"
Bot: "I don't know"  ← ❌ Fail!
```

With memory:
```
User: "My name is Alice"
Bot: "Nice to meet you, Alice!"
User: "What's my name?"
Bot: "Your name is Alice"  ← ✅ Correct!
```

**How it works:**
- Store conversation as list of messages
- Include recent history in each prompt
- Trim old messages to save tokens

**Code:** `src/memory.py`

### 5. PDF Processing

**The pipeline:**

```
PDF File
   │
   ▼
PyPDFLoader (extract text)
   │
   ▼
RecursiveCharacterTextSplitter
   │
   ├──► Chunk 1 (1000 chars)
   ├──► Chunk 2 (1000 chars, 200 char overlap)
   ├──► Chunk 3 (1000 chars, 200 char overlap)
   └──► ...
```

**Why chunk?**
- Smaller chunks = more precise retrieval
- Fits in LLM context window
- Better search results

**Code:** `src/document_processor.py`

---

## 🧪 Testing

### Run Basic Tests

```bash
python tests/test_chatbot.py
```

### Create Sample PDF

```bash
python data/sample_report.py
```

This creates `data/sample_ml_report.pdf` for testing.

### Sample Test Prompts

Upload the sample PDF and try:

1. **Basic questions:**
   - "What is machine learning?"
   - "What are the types of ML?"

2. **Summarization:**
   - "Summarize this document"
   - "What are the main points?"

3. **Follow-up (tests memory):**
   - "What is supervised learning?"
   - "Give me an example"
   - "What about unsupervised?"

4. **Source verification:**
   - "What does the document say about neural networks?"
   - Check the sources expander to verify

---

## ⚠️ Error Handling

The app handles these common errors:

| Error | Cause | Solution |
|-------|-------|----------|
| "API key not found" | Missing .env file | Create .env with OPENAI_API_KEY |
| "PDF not found" | File path issue | Check file exists |
| "No relevant documents" | Empty knowledge base | Upload a PDF first |
| Rate limit | Too many requests | Wait a moment, try again |

**Code:** Error handling is in each module with try-except blocks.

---

## 🎓 Viva Questions (with Answers)

### Q1: What is RAG and why use it?

**Answer:**

RAG stands for **Retrieval-Augmented Generation**. It's a technique where we:
1. Retrieve relevant documents based on the query
2. Augment the LLM prompt with that context
3. Generate an answer using the context

**Why use it?**
- **Knowledge cutoff:** LLMs don't know about recent documents
- **Hallucination:** LLMs make up facts; RAG grounds answers in real documents
- **Custom data:** Can answer questions about your specific PDFs
- **Citations:** Can show where information came from

### Q2: How does FAISS work?

**Answer:**

FAISS is a **vector similarity search** library.

**How it works:**
1. Documents are converted to embedding vectors (using OpenAI's API)
2. Vectors are stored in a FAISS index
3. When searching:
   - Query is converted to embedding
   - FAISS finds nearest neighbors using distance metrics (L2, cosine)
   - Returns most similar vectors quickly

**Why FAISS?**
- Fast: O(log n) search vs O(n) brute force
- In-memory: Very fast lookups
- Free and open source
- Good for small-medium projects

### Q3: Why chunk documents? Why not use the whole PDF?

**Answer:**

**Reasons for chunking:**

1. **Token limits:** LLMs have context limits (4K-128K tokens). Large PDFs won't fit.

2. **Precision:** Smaller chunks = more specific retrieval. If you ask about "neural networks," you get the relevant paragraph, not the whole document.

3. **Noise reduction:** Irrelevant sections don't pollute the context.

4. **Search quality:** Vector search works better with focused, coherent chunks.

**Our approach:**
- Chunk size: 1000 characters
- Overlap: 200 characters (maintains context between chunks)
- Uses RecursiveCharacterTextSplitter (tries to split at natural boundaries)

---

## 🔮 Future Improvements

Realistic enhancements for a future version:

1. **Multiple file formats:** Support Word, TXT, Markdown (not just PDF)
2. **Better chunking:** Use semantic chunking (split at topic boundaries)
3. **Persistent memory:** Save conversations to database (SQLite)
4. **Streaming responses:** Show LLM output as it generates (better UX)
5. **Source highlighting:** Show exact text snippets used
6. **Conversation export:** Save chat as PDF/text file
7. **Multiple LLM support:** Allow switching between GPT-3.5, GPT-4, Claude
8. **Web search:** Add option to search internet + documents

**Out of scope (too complex for semester project):**
- Multi-user support (would need auth, database)
- Docker/Kubernetes deployment
- Cloud hosting (AWS/GCP)
- Real-time collaboration

---

## 📚 What I Learned

This project taught me:

1. **How embeddings work** - Converting meaning to math
2. **Vector databases** - Fast similarity search with FAISS
3. **RAG architecture** - Combining retrieval + generation
4. **LangChain** - Modular framework for LLM apps
5. **Prompt engineering** - How to structure prompts for best results
6. **Chunking strategies** - Balancing context vs precision
7. **Memory management** - Keeping conversation context
8. **Streamlit** - Building UIs without frontend code

---

## 💰 Cost Estimate

Using OpenAI API:

| Operation | Cost |
|-----------|------|
| GPT-3.5 (per 1K tokens) | ~$0.002 |
| Embeddings (per 1K tokens) | ~$0.0001 |
| Processing 10-page PDF | ~$0.02 |
| 1-hour chat session | ~$0.05 |
| **Total for project** | **$1-5** |

> 💡 **Tip:** Use GPT-3.5-turbo, not GPT-4, to save money while learning.

---

## 📝 Project Timeline

**Week 1:**
- Day 1-2: Learn about RAG, FAISS, LangChain
- Day 3-4: Build core modules (embeddings, vector store)
- Day 5-7: Build document processor and chatbot engine

**Week 2:**
- Day 8-9: Build Streamlit UI
- Day 10-11: Testing and bug fixes
- Day 12-13: Documentation (README, comments)
- Day 14: Final review and demo prep

---

## 🙏 Acknowledgments

- **LangChain** - For the excellent framework
- **OpenAI** - For the API and documentation
- **FAISS** - For the fast vector search
- **Streamlit** - For making UI building easy
- **My professor** - For guidance on the project

---

## 📄 License

This is a student project. Feel free to use for learning!

---

## 📧 Contact

For questions about this project, reach out via [your email].

---

**Built with ❤️ for my 4th semester ML course.**

*Last updated: March 2025*
