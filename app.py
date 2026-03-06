"""
Streamlit UI for AI Chatbot with Memory

This is the main entry point for the application.
Run with: streamlit run app.py

Streamlit is perfect for this because:
- Simple Python-only frontend
- Built-in widgets (file upload, chat, buttons)
- Automatic state management
- Easy to deploy
"""

import streamlit as st
import os
import sys

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import our modules
from config import validate_config
from document_processor import DocumentProcessor
from chatbot import RAGChatbot


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# INITIALIZATION
# =============================================================================

def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    
    Session state persists across reruns, so we store:
    - The chatbot instance
    - Chat history for display
    - Processing status
    """
    if "chatbot" not in st.session_state:
        try:
            validate_config()
            st.session_state.chatbot = RAGChatbot()
            st.session_state.initialized = True
        except Exception as e:
            st.session_state.initialized = False
            st.session_state.init_error = str(e)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "processing" not in st.session_state:
        st.session_state.processing = False


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_sidebar():
    """
    Render the sidebar with controls and info.
    """
    with st.sidebar:
        st.title("📚 Document Upload")
        st.markdown("---")
        
        # File upload section
        st.subheader("Upload PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload a PDF to add to the knowledge base"
        )
        
        if uploaded_file is not None:
            if st.button("📥 Process PDF", use_container_width=True):
                process_uploaded_pdf(uploaded_file)
        
        st.markdown("---")
        
        # Knowledge base stats
        st.subheader("Knowledge Base")
        if st.session_state.get("initialized"):
            stats = st.session_state.chatbot.get_stats()
            
            doc_count = stats["vector_store"].get("document_count", 0)
            st.metric("Documents", doc_count)
            
            if st.button("🗑️ Clear Knowledge Base", use_container_width=True):
                st.session_state.chatbot.clear_knowledge_base()
                st.success("Knowledge base cleared!")
                st.rerun()
        
        st.markdown("---")
        
        # Memory controls
        st.subheader("Conversation")
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.get("initialized"):
                st.session_state.chatbot.clear_memory()
            st.rerun()
        
        st.markdown("---")
        
        # About section
        st.subheader("About")
        st.markdown("""
        **AI Chatbot with Memory**
        
        Built with:
        - 🧠 OpenAI GPT-3.5
        - 🔍 FAISS Vector DB
        - 📄 PDF Processing
        - 💬 Conversation Memory
        
        *4th Semester ML Project*
        """)


def process_uploaded_pdf(uploaded_file):
    """
    Process an uploaded PDF file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    """
    try:
        with st.spinner("Processing PDF... This may take a moment."):
            # Initialize processor
            processor = DocumentProcessor()
            
            # Save uploaded file
            file_path = processor.save_uploaded_file(uploaded_file)
            
            # Process PDF (load + chunk)
            chunks = processor.process_pdf(file_path)
            
            # Add to knowledge base
            st.session_state.chatbot.add_documents(chunks)
            
            st.success(f"✅ Processed {len(chunks)} chunks from '{uploaded_file.name}'")
            
    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")


def render_chat_interface():
    """
    Render the main chat interface.
    """
    st.title("🤖 AI Chatbot with Memory")
    st.markdown("*Ask questions about your uploaded documents!*")
    st.markdown("---")
    
    # Check initialization
    if not st.session_state.get("initialized"):
        st.error("⚠️ Configuration Error")
        st.info(f"""
        Please set up your OpenAI API key:
        
        1. Create a `.env` file in the project root
        2. Add: `OPENAI_API_KEY=your_key_here`
        3. Restart the app
        
        Error: {st.session_state.get('init_error', 'Unknown error')}
        """)
        return
    
    # Check if documents exist
    if not st.session_state.chatbot.has_documents():
        st.info("📚 **No documents loaded yet!**\n\nUpload a PDF from the sidebar to get started.")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📎 Sources"):
                    for source in message["sources"]:
                        st.markdown(
                            f"- **{source['source']}** (Page {source['page']}) "
                            f"- Score: {source['score']:.3f}"
                        )
    
    # Chat input
    if prompt := st.chat_input("Ask a question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = st.session_state.chatbot.chat(prompt)
            
            if result["success"]:
                st.markdown(result["answer"])
                
                # Store assistant message
                message_data = {
                    "role": "assistant",
                    "content": result["answer"]
                }
                
                # Add sources if available
                if result.get("sources"):
                    message_data["sources"] = result["sources"]
                    
                    # Show sources in expander
                    with st.expander("📎 Sources"):
                        for source in result["sources"]:
                            st.markdown(
                                f"- **{source['source']}** (Page {source['page']}) "
                                f"- Score: {source['score']:.3f}"
                            )
                
                st.session_state.messages.append(message_data)
            else:
                st.error(result["answer"])


def render_tips_section():
    """
    Render tips and example questions.
    """
    with st.expander("💡 Tips & Example Questions"):
        st.markdown("""
        **How to use this chatbot:**
        
        1. **Upload a PDF** using the sidebar
        2. **Wait for processing** (you'll see a success message)
        3. **Ask questions** about the document content
        
        **Example Questions:**
        - "What is the main topic of this document?"
        - "Summarize the key points"
        - "What does the author say about [topic]?"
        - "List the main findings"
        - "Explain the conclusion"
        
        **Features:**
        - ✅ Remembers conversation context
        - ✅ Cites sources from the PDF
        - ✅ Shows relevance scores
        - ✅ Handles follow-up questions
        
        **Limitations:**
        - Only answers based on uploaded documents
        - May struggle with very large PDFs
        - Requires clear, specific questions
        """)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """
    Main application entry point.
    """
    # Initialize
    initialize_session_state()
    
    # Render UI components
    render_sidebar()
    render_chat_interface()
    render_tips_section()


if __name__ == "__main__":
    main()
