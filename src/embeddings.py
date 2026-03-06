"""
Embeddings Module

This module handles converting text into vector embeddings.

WHAT ARE EMBEDDINGS?
====================
Embeddings are numerical representations of text. Think of them
as coordinates in a high-dimensional space (usually 384-1536 dimensions).

Similar texts have similar embeddings (vectors point in similar
directions). This is the magic that makes semantic search work!

FREE OPTIONS:
=============
1. HuggingFace (Recommended - FREE!)
   - Uses open-source models
   - No API key needed
   - Runs locally on your machine
   - Default: "sentence-transformers/all-MiniLM-L6-v2" (384 dimensions)

2. OpenAI (Paid)
   - text-embedding-ada-002
   - 1536 dimensions
   - Requires API key and payment
"""

from typing import List
from langchain_core.documents import Document

# Import config
from config import (
    get_embedding_config,
    EMBEDDING_PROVIDER,
    HUGGINGFACE_EMBEDDING_MODEL,
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL
)


class EmbeddingGenerator:
    """
    Generates embeddings for text using FREE HuggingFace models
    or OpenAI's API (if configured).
    
    This is a unified interface that works with both providers.
    """
    
    def __init__(self):
        """
        Initialize the embedding model based on configuration.
        """
        self.config = get_embedding_config()
        self.provider = self.config["provider"]
        
        if self.provider == "huggingface":
            self._init_huggingface()
        elif self.provider == "openai":
            self._init_openai()
        else:
            raise ValueError(f"Unknown embedding provider: {self.provider}")
    
    def _init_huggingface(self):
        """
        Initialize HuggingFace embeddings (FREE!).
        
        This downloads the model on first use (~80MB).
        After that, it runs completely offline!
        """
        from langchain_huggingface import HuggingFaceEmbeddings
        
        print(f"🔮 Loading HuggingFace model: {self.config['model']}")
        print("   (First run will download ~80MB model...)")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config["model"],
            model_kwargs={'device': 'cpu'},  # Use CPU (works on all machines)
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print("✅ HuggingFace embeddings ready (FREE!)")
    
    def _init_openai(self):
        """
        Initialize OpenAI embeddings (paid).
        """
        from langchain_openai import OpenAIEmbeddings
        
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found! Check your .env file.")
        
        self.embeddings = OpenAIEmbeddings(
            model=OPENAI_EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        
        print(f"🔮 OpenAI embeddings loaded: {OPENAI_EMBEDDING_MODEL}")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Convert a single text string to embedding vector.
        
        Args:
            text: The text to embed
            
        Returns:
            List of floats (the embedding vector)
        """
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """
        Convert multiple documents to embedding vectors.
        
        This is more efficient than calling embed_text multiple times
        because it batches the processing.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of embedding vectors (one per document)
        """
        texts = [doc.page_content for doc in documents]
        return self.embeddings.embed_documents(texts)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of text strings.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)


# =============================================================================
# EXPLANATION: How embeddings work with FREE HuggingFace
# =============================================================================
"""
HUGGINGFACE EMBEDDINGS (FREE):
==============================

Model: sentence-transformers/all-MiniLM-L6-v2
- Size: ~80MB
- Dimensions: 384 (smaller than OpenAI's 1536)
- Speed: Fast on CPU
- Quality: Very good for most tasks!
- Cost: FREE forever!

How it works:
1. First time: Downloads model from HuggingFace Hub
2. Subsequent runs: Uses cached model (offline!)
3. Runs entirely on your CPU
4. No API calls, no rate limits, no payments!

WHY THIS MODEL?
- Trained on sentence similarity tasks
- Optimized for semantic search
- Small and fast
- Open source (Apache 2.0 license)

COMPARISON:
===========
                 HuggingFace (Free)    OpenAI (Paid)
Price            FREE                  $0.0001/1K tokens
Dimensions       384                   1536
Quality          ⭐⭐⭐⭐                ⭐⭐⭐⭐⭐
Speed (local)    ⚡⚡⚡⚡⚡              🌐 (network)
Privacy          ✅ Local              ❌ Sent to API
"""


if __name__ == "__main__":
    # Quick test
    embedder = EmbeddingGenerator()
    
    test_text = "This is a test sentence about machine learning."
    embedding = embedder.embed_text(test_text)
    
    print(f"\nTest text: {test_text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {[round(x, 4) for x in embedding[:5]]}")
    print(f"\n✅ Embeddings working! Provider: {embedder.provider}")
