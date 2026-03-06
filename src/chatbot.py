from typing import List, Dict, Tuple
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from config import (
    get_llm_config,
    LLM_TEMPERATURE,
    MAX_TOKENS,
    TOP_K_RETRIEVAL
)

from vector_store import VectorStore
from memory import ConversationMemory


class RAGChatbot:

    def __init__(self):

        self.vector_store = VectorStore()
        self.memory = ConversationMemory()

        self.llm_config = get_llm_config()

        self.llm = self._initialize_llm()

        self.rag_prompt = self._create_rag_prompt()

        print("🤖 Chatbot initialized successfully!")

    # --------------------------------------------------

    def _initialize_llm(self):

        provider = self.llm_config["provider"]

        if provider == "groq":
            return self._init_groq()

        elif provider == "ollama":
            return self._init_ollama()

        elif provider == "openai":
            return self._init_openai()

        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    # --------------------------------------------------

    def _init_groq(self):

        from langchain_groq import ChatGroq

        api_key = self.llm_config["api_key"]

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found!\n"
                "Get FREE key from: https://console.groq.com/keys"
            )

        model = self.llm_config.get("model", "llama-3.1-8b-instant")

        print(f"🚀 Initializing Groq with model: {model}")

        return ChatGroq(
            model=model,
            temperature=LLM_TEMPERATURE,
            max_tokens=MAX_TOKENS,
            groq_api_key=api_key
        )

    # --------------------------------------------------

    def _init_ollama(self):

        from langchain_ollama import ChatOllama

        base_url = self.llm_config["base_url"]
        model = self.llm_config["model"]

        print(f"🖥️ Initializing Ollama")
        print(f"Model: {model}")

        return ChatOllama(
            model=model,
            base_url=base_url,
            temperature=LLM_TEMPERATURE
        )

    # --------------------------------------------------

    def _init_openai(self):

        from langchain_openai import ChatOpenAI

        api_key = self.llm_config["api_key"]

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found!")

        return ChatOpenAI(
            model=self.llm_config["model"],
            temperature=LLM_TEMPERATURE,
            max_tokens=MAX_TOKENS,
            openai_api_key=api_key
        )

    # --------------------------------------------------

    def _create_rag_prompt(self) -> PromptTemplate:

        template = """You are a helpful AI assistant.

Use the CONTEXT to answer the question.

If the answer is not in the context say:
"I don't have enough information."

CONTEXT
{context}

CONVERSATION HISTORY
{history}

QUESTION
{question}

ANSWER
"""

        return PromptTemplate(
            template=template,
            input_variables=["context", "history", "question"]
        )

    # --------------------------------------------------

    def _format_context(self, documents: List[Tuple[Document, float]]) -> str:

        if not documents:
            return "No relevant documents found."

        context_parts = []

        for i, (doc, score) in enumerate(documents, 1):

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")

            context_parts.append(
                f"[Doc {i} | Source: {source} | Page: {page} | Score: {score:.3f}]\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(context_parts)

    # --------------------------------------------------

    def chat(self, question: str) -> Dict:

        try:

            retrieved_docs = self.vector_store.search(
                question,
                k=TOP_K_RETRIEVAL
            )

            context = self._format_context(retrieved_docs)

            history = self.memory.get_context_string(n=3)

            prompt = self.rag_prompt.format(
                context=context,
                history=history,
                question=question
            )

            response = self.llm.invoke(prompt)

            answer = response.content

            self.memory.add_user_message(question)
            self.memory.add_assistant_message(answer)

            return {
                "success": True,
                "answer": answer,
                "retrieved_chunks": len(retrieved_docs),
                "llm_provider": self.llm_config["provider"]
            }

        except Exception as e:

            return {
                "success": False,
                "answer": f"Error: {str(e)}"
            }

    # --------------------------------------------------

    def add_documents(self, documents: List[Document]):

        self.vector_store.add_documents(documents)

    def clear_memory(self):

        self.memory.clear()

    def clear_knowledge_base(self):

        self.vector_store.clear()

    def get_stats(self):

        return {
            "llm_provider": self.llm_config["provider"],
            "llm_model": self.llm_config["model"],
            "memory": self.memory.get_stats(),
            "vector_store": self.vector_store.get_stats()
        }

    def has_documents(self):

        stats = self.vector_store.get_stats()

        return stats.get("document_count", 0) > 0


if __name__ == "__main__":

    bot = RAGChatbot()

    print(bot.get_stats())