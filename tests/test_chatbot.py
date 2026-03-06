"""
Simple tests for the chatbot.

Run with: python tests/test_chatbot.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import get_llm_config, get_embedding_config


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from config import validate_config, get_llm_config, get_embedding_config
        from document_processor import DocumentProcessor
        from embeddings import EmbeddingGenerator
        from vector_store import VectorStore
        from memory import ConversationMemory
        from chatbot import RAGChatbot
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_embeddings():
    """Test embedding generation (FREE HuggingFace)."""
    print("\nTesting HuggingFace embeddings (FREE)...")
    
    try:
        from embeddings import EmbeddingGenerator
        
        print("   (First run downloads ~80MB model...)")
        embedder = EmbeddingGenerator()
        
        test_text = "This is a test about machine learning."
        embedding = embedder.embed_text(test_text)
        
        assert len(embedding) > 0, "Embedding is empty"
        assert isinstance(embedding, list), "Embedding is not a list"
        
        print(f"✅ Embeddings work! Dimension: {len(embedding)}")
        print(f"   Provider: {embedder.provider}")
        return True
    except Exception as e:
        print(f"❌ Embedding test failed: {e}")
        return False


def test_memory():
    """Test conversation memory."""
    print("\nTesting memory...")
    
    try:
        from memory import ConversationMemory
        
        memory = ConversationMemory(max_length=3)
        
        # Add messages
        memory.add_user_message("Hello!")
        memory.add_assistant_message("Hi there!")
        memory.add_user_message("How are you?")
        
        # Check history
        history = memory.get_history()
        assert len(history) == 3, f"Expected 3 messages, got {len(history)}"
        
        # Check stats
        stats = memory.get_stats()
        assert stats["exchanges"] == 1, "Exchange count wrong"
        
        print("✅ Memory works!")
        return True
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        return False


def test_document_processor():
    """Test document processor (without actual PDF)."""
    print("\nTesting document processor...")
    
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        
        # Test that it's initialized
        assert processor.text_splitter is not None
        
        print("✅ Document processor initialized!")
        return True
    except Exception as e:
        print(f"❌ Document processor test failed: {e}")
        return False


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        llm_config = get_llm_config()
        embed_config = get_embedding_config()
        
        print(f"   LLM Provider: {llm_config['provider']}")
        print(f"   LLM Model: {llm_config['model']}")
        print(f"   Embedding Provider: {embed_config['provider']}")
        print(f"   Embedding Model: {embed_config['model']}")
        
        print("✅ Configuration loaded!")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False


def print_free_setup_guide():
    """Print guide for free setup."""
    print("\n" + "="*60)
    print("FREE API SETUP GUIDE")
    print("="*60)
    print("""
To use this chatbot for FREE:

OPTION 1: Groq (Recommended - Easiest)
----------------------------------------
1. Get FREE API key: https://console.groq.com/keys
2. Add to .env: GROQ_API_KEY=gsk_your_key
3. Set: LLM_PROVIDER=groq
4. Cost: $0 (1M tokens/day free!)

OPTION 2: Ollama (100% FREE - Local)
-------------------------------------
1. Download: https://ollama.com/download
2. Run: ollama pull llama3.2
3. Run: ollama serve
4. Set: LLM_PROVIDER=ollama
5. Cost: $0 forever (runs locally!)

EMBEDDINGS (Always FREE)
------------------------
Using HuggingFace embeddings - no setup needed!
Downloads once (~80MB), runs offline forever.
""")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AI Chatbot Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_document_processor,
        test_memory,
        test_embeddings,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check errors above.")
    
    print_free_setup_guide()
    
    return all(results)


if __name__ == "__main__":
    run_all_tests()
