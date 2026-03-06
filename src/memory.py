"""
Memory Module

This module handles conversation history and context management.

WHAT IS MEMORY IN A CHATBOT?
============================
Memory allows the chatbot to remember previous parts of the conversation.
Without memory, each question is treated as completely independent.

Example WITHOUT memory:
User: "My name is Alice"
Bot: "Nice to meet you!"
User: "What's my name?"
Bot: "I don't know." ❌

Example WITH memory:
User: "My name is Alice"
Bot: "Nice to meet you, Alice!"
User: "What's my name?"
Bot: "Your name is Alice." ✅

TYPES OF MEMORY:
================
1. Conversation Buffer: Stores raw conversation history
2. Conversation Summary: Summarizes long conversations
3. Entity Memory: Remembers specific facts about user
4. Vector Memory: Retrieves relevant past messages (advanced)

For this project, we use a simple buffer with a limit.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from config import MAX_HISTORY_LENGTH


@dataclass
class Message:
    """
    Represents a single message in the conversation.
    
    Using a dataclass makes it clean and easy to work with.
    """
    role: str  # "user" or "assistant"
    content: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format for LLM APIs."""
        return {"role": self.role, "content": self.content}


class ConversationMemory:
    """
    Manages conversation history.
    
    This is essentially a smart list that:
    - Stores messages in order
    - Limits total length (to save tokens)
    - Formats history for the LLM
    """
    
    def __init__(self, max_length: int = MAX_HISTORY_LENGTH):
        """
        Initialize memory.
        
        Args:
            max_length: Maximum number of message pairs to keep
        """
        self.max_length = max_length
        self.messages: List[Message] = []
        
        print(f"🧠 Memory initialized (max {max_length} exchanges)")
    
    def add_user_message(self, content: str):
        """
        Add a user message to memory.
        
        Args:
            content: The user's message
        """
        self.messages.append(Message(role="user", content=content))
        self._trim_if_needed()
    
    def add_assistant_message(self, content: str):
        """
        Add an assistant (bot) message to memory.
        
        Args:
            content: The bot's response
        """
        self.messages.append(Message(role="assistant", content=content))
        self._trim_if_needed()
    
    def _trim_if_needed(self):
        """
        Remove oldest messages if we exceed max_length.
        
        We keep pairs of messages (user + assistant), so we
        remove 2 messages at a time to maintain conversation flow.
        """
        # Each "exchange" is 2 messages (user + assistant)
        max_messages = self.max_length * 2
        
        while len(self.messages) > max_messages:
            # Remove oldest messages (from the beginning)
            removed = self.messages.pop(0)
            print(f"🗑️ Trimmed old message: {removed.role}")
    
    def get_history(self, n: int = None) -> List[Message]:
        """
        Get conversation history.
        
        Args:
            n: Number of most recent messages to return (None = all)
            
        Returns:
            List of Message objects
        """
        if n is None:
            return self.messages.copy()
        return self.messages[-n:].copy()
    
    def get_formatted_history(self, n: int = None) -> List[Dict[str, str]]:
        """
        Get history formatted for OpenAI API.
        
        Returns:
            List of dicts with 'role' and 'content' keys
        """
        messages = self.get_history(n)
        return [msg.to_dict() for msg in messages]
    
    def get_context_string(self, n: int = 4) -> str:
        """
        Get recent history as a single string.
        
        This is useful for including in RAG prompts.
        
        Args:
            n: Number of recent exchanges to include
            
        Returns:
            Formatted conversation string
        """
        recent = self.get_history(n * 2)  # n exchanges = 2n messages
        
        lines = []
        for msg in recent:
            prefix = "User: " if msg.role == "user" else "Assistant: "
            lines.append(f"{prefix}{msg.content}")
        
        return "\n".join(lines)
    
    def clear(self):
        """Clear all conversation history."""
        self.messages = []
        print("🧹 Memory cleared")
    
    def is_empty(self) -> bool:
        """Check if memory is empty."""
        return len(self.messages) == 0
    
    def get_stats(self) -> Dict:
        """
        Get memory statistics.
        
        Returns:
            Dict with memory info
        """
        return {
            "total_messages": len(self.messages),
            "exchanges": len(self.messages) // 2,
            "max_exchanges": self.max_length,
            "is_empty": self.is_empty()
        }


# =============================================================================
# EXPLANATION: Memory in RAG Context
# =============================================================================
"""
HOW MEMORY FITS INTO RAG:
=========================

Standard RAG (no memory):
-------------------------
User: "What is it used for?"
Retrieved: [chunks about ML]
LLM sees: "What is it used for?" + chunks
Problem: "it" is ambiguous without context!

RAG with Memory:
----------------
Previous: "Machine learning is a type of AI..."
User: "What is it used for?"
Retrieved: [chunks about ML applications]
LLM sees: "Machine learning is a type of AI... What is it used for?" + chunks
Result: LLM knows "it" = machine learning! ✅

MEMORY + RAG PROMPT STRUCTURE:
==============================

System: You are a helpful assistant...

Context: [Retrieved chunks from PDF]

Conversation History:
User: Hello
Assistant: Hi! How can I help?
User: Tell me about the report
Assistant: [Previous answer]

Current Question: What are the main findings?

Answer:
"""


if __name__ == "__main__":
    # Test memory
    memory = ConversationMemory(max_length=3)
    
    memory.add_user_message("Hello!")
    memory.add_assistant_message("Hi there!")
    memory.add_user_message("What's your name?")
    
    print("History:", memory.get_formatted_history())
    print("Stats:", memory.get_stats())
