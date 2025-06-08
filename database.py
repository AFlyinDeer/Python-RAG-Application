import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Uncomment the line below to debug embeddings
from debug_embeddings import DebugOllamaEmbeddings as OllamaEmbeddings

# Configuration
DB_DIR = r"F:\Code\RAGProject\RAG\instance"
COLLECTION_NAME = "pdf_docs"
EMBEDDING_MODEL = "nomic-embed-text"

def load_vectorstore():
    """Load existing Chroma vectorstore"""
    if not os.path.exists(DB_DIR):
        raise ValueError(f"Database not found at {DB_DIR}. Run db_setup.py first.")
    
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    
    count = vectorstore._collection.count()
    if count == 0:
        raise ValueError("Database is empty. Run db_setup.py first.")
    
    # Debugging
    #print(f"Loaded {count} documents")
    return vectorstore

def create_vectorstore():
    """Create new Chroma vectorstore"""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    
    return vectorstore

def check_database():
    """Check database status - returns info without throwing errors"""
    if not os.path.exists(DB_DIR):
        return False, "Database not found"
    
    try:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=DB_DIR
        )
        
        count = vectorstore._collection.count()
        if count == 0:
            return False, "Database empty"
        
        from file_processing import get_processed_files
        processed_files = get_processed_files(vectorstore)
        return True, f"{count} documents from {len(processed_files)} files"
        
    except Exception as e:
        return False, f"Error: {e}"