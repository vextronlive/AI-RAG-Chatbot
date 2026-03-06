"""
Document Processor Module

This module handles loading and processing PDF files.
When a user uploads a PDF, we need to:
1. Load the PDF
2. Extract text from it
3. Split it into manageable chunks
4. Return those chunks for embedding

Why chunking? LLMs have token limits, and searching through
massive documents is inefficient. Smaller chunks work better.
"""

import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Import our config
from config import CHUNK_SIZE, CHUNK_OVERLAP, UPLOAD_DIR


class DocumentProcessor:
    """
    Handles all document processing operations.
    
    Think of this as the 'librarian' - it takes messy PDFs
    and organizes them into clean, searchable chunks.
    """
    
    def __init__(self):
        """Initialize the text splitter with config settings."""
        # RecursiveCharacterTextSplitter is smart - it tries to split
        # at natural boundaries (paragraphs, sentences) first
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_pdf(self, pdf_path: str) -> List[Document]:
        """
        Load a PDF file and extract all text.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of Document objects (one per page)
            
        Raises:
            FileNotFoundError: If PDF doesn't exist
            Exception: If PDF is corrupted or unreadable
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        try:
            # PyPDFLoader handles the heavy lifting of PDF parsing
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            
            print(f"📄 Loaded PDF: {len(pages)} pages")
            return pages
            
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks.
        
        Why chunk?
        - FAISS works better with smaller pieces
        - More precise retrieval (find exact relevant section)
        - Fits within LLM context window
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        if not documents:
            return []
        
        # The splitter maintains metadata (like page numbers) automatically
        chunks = self.text_splitter.split_documents(documents)
        
        print(f"✂️ Split into {len(chunks)} chunks")
        return chunks
    
    def process_pdf(self, pdf_path: str) -> List[Document]:
        """
        Complete PDF processing pipeline.
        
        This is the main method to call - it loads AND chunks
        the PDF in one go.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of text chunks ready for embedding
        """
        # Step 1: Load the PDF
        pages = self.load_pdf(pdf_path)
        
        # Step 2: Split into chunks
        chunks = self.split_documents(pages)
        
        # Add source information to each chunk's metadata
        # This helps us trace back where info came from
        for chunk in chunks:
            chunk.metadata["source"] = os.path.basename(pdf_path)
        
        return chunks
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """
        Save an uploaded file (from Streamlit) to disk.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Path where file was saved
        """
        # Create safe filename
        filename = uploaded_file.name.replace(" ", "_")
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Write the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        print(f"💾 Saved uploaded file: {file_path}")
        return file_path


# Simple test if run directly
if __name__ == "__main__":
    processor = DocumentProcessor()
    print("Document Processor initialized successfully!")
    print(f"Chunk size: {CHUNK_SIZE}, Overlap: {CHUNK_OVERLAP}")
