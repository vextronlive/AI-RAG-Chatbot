# 🆓 FREE APIs Guide - AI Chatbot with Memory

> Is project mein bilkul **FREE** APIs use kar sakte ho! Koi payment nahi chahiye! 💰

---

## 🎯 Sabse Easy Option: Groq (Recommended)

### Kya hai?
- **Groq** ek AI company hai jo super fast LLM inference provide karti hai
- Unka **FREE tier** hai: **1,000,000 tokens per day**
- Tumhari semester project ke liye bahut zyada hai!

### Setup (2 minutes)

#### Step 1: API Key Le Lo (FREE)

1. Jao: **[console.groq.com](https://console.groq.com/keys)**
2. Sign up karo (email ya GitHub se - FREE hai)
3. "Create API Key" pe click karo
4. Key copy karo (starts with `gsk_`)

#### Step 2: Project Configure Karo

`.env` file mein likho:
```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here
EMBEDDING_PROVIDER=huggingface
```

Bas! Done! 🎉

### Groq Ke Models

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `llama3-8b-8192` | ⚡ Fast | ⭐⭐⭐⭐ | Default - best balance |
| `llama3-70b-8192` | 🐢 Slow | ⭐⭐⭐⭐⭐ | Better quality |
| `mixtral-8x7b-32768` | ⚡ Fast | ⭐⭐⭐⭐ | Long context |

**Recommendation:** `llama3-8b-8192` use karo - fast aur achha quality!

### Free Tier Limits

- **1,000,000 tokens per day** (bahut zyada!)
- **20 requests per minute**
- **Cost: $0** ✅

---

## 🖥️ 100% FREE Option: Ollama (Local)

### Kya hai?
- **Ollama** tumhare computer pe LLM chalata hai
- **Bilkul FREE** - koi API call nahi, koi limit nahi!
- Internet bhi nahi chahiye baad mein

### Setup

#### Step 1: Ollama Download Karo

Website: **[ollama.com/download](https://ollama.com/download)**

Windows/Mac/Linux sabke liye available hai.

#### Step 2: Model Download Karo

Terminal mein run karo:
```bash
# Small model (~2GB) - fast
ollama pull llama3.2

# Ya medium model (~4GB) - better quality
ollama pull mistral
```

#### Step 3: Server Start Karo

```bash
ollama serve
```

Ye command chalta rehna chahiye. Alag terminal mein chalao.

#### Step 4: Project Configure Karo

`.env` file mein likho:
```
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
EMBEDDING_PROVIDER=huggingface
# API key nahi chahiye!
```

### Ollama Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `llama3.2` | ~2GB | ⚡ Fast | ⭐⭐⭐⭐ |
| `mistral` | ~4GB | 🐢 Medium | ⭐⭐⭐⭐⭐ |
| `phi3` | ~2GB | ⚡ Fast | ⭐⭐⭐⭐ |
| `gemma2` | ~3GB | 🐢 Medium | ⭐⭐⭐⭐ |

**Recommendation:** `llama3.2` - small, fast, achha quality!

### Pros & Cons

**✅ Pros:**
- Bilkul FREE forever
- Fully private (data nahi jaata kahi)
- No internet needed after setup
- No rate limits

**❌ Cons:**
- Pehli baar model download karna padta hai (~2-4GB)
- CPU pe chalta hai (thoda slow ho sakta hai)
- Server manually start karna padta hai

---

## 🔮 Embeddings (Hamesha FREE)

Embeddings ke liye hum **HuggingFace** use karte hai - bilkul FREE!

### Kya chahiye?
- **Koi API key nahi chahiye!**
- Pehli baar model download hota hai (~80MB)
- Uske baad offline kaam karta hai

### Kaam kaise karta hai?
```python
# Text ko numbers mein convert karta hai
"Machine learning is amazing" → [0.23, -0.45, 0.89, ...]
```

Similar text = similar numbers (yehi magic hai!)

### Default Model
- **Name:** `sentence-transformers/all-MiniLM-L6-v2`
- **Size:** ~80MB
- **Dimensions:** 384
- **Quality:** Bahut achha!

---

## 📊 Comparison Table

| Feature | Groq | Ollama | OpenAI |
|---------|------|--------|--------|
| **Cost** | FREE | FREE | Paid |
| **Speed** | ⚡ Very Fast | 🐢 Medium | ⚡ Fast |
| **Setup** | Easy | Medium | Easy |
| **Internet** | Required | After setup: No | Required |
| **Privacy** | Data goes to API | 100% Private | Data goes to API |
| **Rate Limit** | 1M tokens/day | No limit | Pay per use |
| **Best For** | Beginners | Privacy/Offline | Production |

---

## 🎓 Recommendation for Students

### Agar tum beginner ho:
**Groq use karo!**
- 2 minute setup
- Super fast
- Free tier bahut zyada hai
- Bas API key daalo aur chalu!

### Agar privacy chahiye ya slow internet hai:
**Ollama use karo!**
- Ek baar setup karo
- Uske baad bilkul free
- Internet bhi nahi chahiye

---

## ⚠️ Common Issues

### Groq Issues

| Problem | Solution |
|---------|----------|
| "Invalid API key" | Key sahi copy karo (starts with `gsk_`) |
| "Rate limit exceeded" | Thodi der wait karo (20 req/min limit) |
| "Model not found" | `.env` mein sahi model name likho |

### Ollama Issues

| Problem | Solution |
|---------|----------|
| "Connection refused" | `ollama serve` chalu hai? Check karo |
| "Model not found" | `ollama pull llama3.2` run karo |
| Slow responses | Normal hai - CPU pe chal raha hai |

### HuggingFace Embeddings Issues

| Problem | Solution |
|---------|----------|
| First run slow | Model download ho raha hai (~80MB) - wait karo |
| Out of memory | Chhota model use karo |

---

## 💡 Pro Tips

1. **Start with Groq** - Sabse easy hai
2. **Embeddings automatic** - Kuch setup nahi chahiye
3. **Test karo** - Sample PDF upload karke dekh lo
4. **Switch kar sakte ho** - Groq se Ollama mein easily switch

---

## 📞 Need Help?

Groq: [console.groq.com](https://console.groq.com)  
Ollama: [ollama.com](https://ollama.com)  
HuggingFace: [huggingface.co](https://huggingface.co)

---

**Happy Coding! 🚀**

*Koi payment nahi, sirf FREE APIs!* ✅
