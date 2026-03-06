"""
Vector Store Module (FAISS)

This module handles the vector database using FAISS.

WHAT IS FAISS?
==============
FAISS (Facebook AI Similarity Search) is a library for efficient
similarity search and clustering of dense vectors.

Think of it as a super-fast index for finding similar embeddings.
Instead of comparing your query with every document (O(n)),
FAISS can do it in O(log n) or even O(1) with some tradeoffs.

WHY FAISS?
==========
- Fast: Optimized C++ backend
- In-memory: Super quick lookups
- Free: Open source
- Simple: Easy to save/load indexes
- Good for: Small to medium projects (up to millions of vectors)

LIMITATIONS:
- In-memory only (data lost if not saved)
- Not distributed (single machine)
- For production scale, consider Pinecone/Weaviate
"""

import os
import pickle
from typing import List, Optional, Tuple
import numpy as np
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

# Import our modules
from embeddings import EmbeddingGenerator
from config import VECTOR_STORE_PATH, TOP_K_RETRIEVAL


class VectorStore:
    """
    Manages the FAISS vector database.
    
    This class provides a clean interface for:
    - Adding documents to the index
    - Searching for similar documents
    - Saving/loading the index
    """
    
    def __init__(self):
        """
        Initialize the vector store.
        
        Creates an empty store or loads existing one.
        """
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store: Optional[FAISS] = None
        
        # Try to load existing index
        self._load_or_create()
    
    def _load_or_create(self):
        """
        Load existing FAISS index or create new one.
        
        This is called automatically on initialization.
        """
        if os.path.exists(VECTOR_STORE_PATH):
            try:
                self.load()
                print("📚 Loaded existing vector store")
            except Exception as e:
                print(f"⚠️ Could not load existing store: {e}")
                print("🆕 Creating new vector store")
                self.vector_store = None
        else:
            print("🆕 No existing store found. Will create on first add.")
            self.vector_store = None
    
    def add_documents(self, documents: List[Document]):
        """
        Add documents to the vector store.
        
        This process:
        1. Generates embeddings for all documents
        2. Adds them to the FAISS index
        3. Associates embeddings with document content
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            print("⚠️ No documents to add")
            return
        
        print(f"🔄 Adding {len(documents)} documents to vector store...")
        
        if self.vector_store is None:
            # First time - create new index
            # FAISS.from_documents handles embedding generation internally
            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embedding_generator.embeddings
            )
            print("✅ Created new FAISS index")
        else:
            # Add to existing index
            self.vector_store.add_documents(documents)
            print(f"✅ Added to existing index")
        
        # Auto-save after adding
        self.save()
    
    def search(self, query: str, k: int = None) -> List[Tuple[Document, float]]:
        """
        Search for documents similar to the query.
        
        This is the core RAG retrieval step!
        
        Args:
            query: The search query (user question)
            k: Number of results to return (default: TOP_K_RETRIEVAL)
            
        Returns:
            List of (document, similarity_score) tuples
            Higher score = more similar (range: 0 to 1 typically)
        """
        if self.vector_store is None:
            print("⚠️ Vector store is empty! Add documents first.")
            return []
        
        k = k or TOP_K_RETRIEVAL
        
        # similarity_search_with_score returns (doc, score) tuples
        # score is L2 distance (lower is better), but we convert to similarity
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        print(f"🔍 Found {len(results)} relevant chunks")
        return results
    
    def save(self):
        """
        Save the FAISS index to disk.
        
        FAISS is in-memory, so we MUST save or lose data!
        """
        if self.vector_store is None:
            print("⚠️ Nothing to save")
            return
        
        # Create directory if needed
        os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
        
        # Save FAISS index
        self.vector_store.save_local(VECTOR_STORE_PATH)
        print(f"💾 Saved vector store to {VECTOR_STORE_PATH}")
    
    def load(self):
        """
        Load FAISS index from disk.
        
        Raises:
            Exception: If index file is corrupted or missing
        """
        if not os.path.exists(VECTOR_STORE_PATH):
            raise FileNotFoundError(f"No index found at {VECTOR_STORE_PATH}")
        
        self.vector_store = FAISS.load_local(
            VECTOR_STORE_PATH,
            self.embedding_generator.embeddings,
            allow_dangerous_deserialization=True  # Safe since we created it
        )
        print(f"📂 Loaded vector store from {VECTOR_STORE_PATH}")
    
    def clear(self):
        """
        Clear all documents from the store.
        
        Use with caution - this deletes all data!
        """
        self.vector_store = None
        if os.path.exists(VECTOR_STORE_PATH):
            os.remove(VECTOR_STORE_PATH)
        print("🗑️ Vector store cleared")
    
    def get_stats(self) -> dict:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with store info
        """
        if self.vector_store is None:
            return {"status": "empty", "document_count": 0}
        
        # FAISS doesn't expose count directly, so we estimate
        # by checking the index size
        index = self.vector_store.index
        return {
            "status": "loaded",
            "document_count": index.ntotal,
            "index_type": type(index).__name__
        }


# =============================================================================
# EXPLANATION: How FAISS Search Works
# =============================================================================
"""
FAISS SEARCH PROCESS:
====================

1. User Query: "What is machine learning?"

2. Embed Query: Convert to vector [0.1, -0.5, 0.3, ...]

3. FAISS Search:
   - Uses Approximate Nearest Neighbor (ANN) search
   - Pre-built index structure for fast lookup
   - Common index types: Flat (exact), IVF (inverted file), HNSW (graph)

4. Return Results:
   - Top-k most similar vectors
   - Associated document chunks
   - Similarity scores

INDEX TYPES (FAISS):
- IndexFlatL2: Exact search, slow but accurate
- IndexIVFFlat: Approximate, faster, good balance
- IndexHNSW: Graph-based, very fast, slightly less accurate

For this project, LangChain uses IndexFlatL2 by default (simple & accurate).
"""


if __name__ == "__main__":
    # Test the vector store
    store = VectorStore()
    print(f"Store stats: {store.get_stats()}")
