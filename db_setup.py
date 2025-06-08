import os
import gc
from database import create_vectorstore, check_database
from file_processing import get_processed_files, load_and_split_documents, get_document_files

# Configuration
DOCS_DIR = r"F:\Code\RAGProject\RAG\documents"
CHUNK_SIZE = 800
OVERLAP = 100

def setup_database():
    """Main setup function"""
    # Import DB_DIR from database module
    from database import DB_DIR
    
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)  # Make sure DB directory exists
    
    # Get all document files (PDF and DOCX)
    all_document_files = get_document_files(DOCS_DIR)
    
    if not all_document_files:
        print(f"No PDF or DOCX files found in {DOCS_DIR}")
        return False
    
    # Create vectorstore
    vectorstore = create_vectorstore()
    current_count = vectorstore._collection.count()
    
    if current_count > 0:
        # Check for new files
        processed_files = get_processed_files(vectorstore)
        new_files = [f for f in all_document_files if f not in processed_files]
        
        if not new_files:
            print(f"Database up to date with {current_count} documents from {len(processed_files)} files")
            return True
        
        print(f"Found {len(new_files)} new files to add to existing database")
        files_to_process = new_files
    else:
        print(f"Creating new database with {len(all_document_files)} files")
        files_to_process = all_document_files
    
    # Process files
    documents = load_and_split_documents(DOCS_DIR, files_to_process, CHUNK_SIZE, OVERLAP)
    
    if documents:
        print(f"Adding {len(documents)} chunks to database...")
        
        # Add in batches
        batch_size = 50
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            vectorstore.add_documents(batch)
            gc.collect()
        
        final_count = vectorstore._collection.count()
        print(f"** Database updated: {current_count} -> {final_count} documents **")
    
    return True

if __name__ == "__main__":
    print("PDF Database Setup")
    print("-" * 20)
    
    exists, status = check_database()
    print(f"Status: {status}")
    
    if setup_database():
        print("Setup complete!")
    else:
        print("Setup failed")