import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import docx2txt

def get_processed_files(vectorstore):
    """Get list of files already in database"""
    try:
        docs = vectorstore.get(include=['metadatas'])
        return {meta['source_file'] for meta in docs['metadatas'] 
                if meta and 'source_file' in meta}
    except:
        return set()

def load_and_split_documents(docs_dir, files_to_process, chunk_size=800, overlap=100):
    """Load and split PDF/DOCX files"""
    if not files_to_process:
        return []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    
    documents = []
    processed = 0
    
    for filename in files_to_process:
        filepath = os.path.join(docs_dir, filename)
        ext = os.path.splitext(filename)[1].lower()
        
        print(f"Processing: {filename}")
        
        try:
            if ext == '.pdf':
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                splits = splitter.split_documents(docs)
                
                for doc in splits:
                    doc.metadata = {
                        'source_file': filename,
                        'page': doc.metadata.get('page', 0),
                        'file_type': 'pdf'
                    }
                documents.extend(splits)
                processed += 1
                
            elif ext == '.docx':
                content = docx2txt.process(filepath)
                if content and content.strip():
                    doc = Document(page_content=content.strip())
                    splits = splitter.split_documents([doc])
                    
                    for i, split in enumerate(splits):
                        split.metadata = {
                            'source_file': filename,
                            'page': i + 1,
                            'file_type': 'docx'
                        }
                    documents.extend(splits)
                    processed += 1
                else:
                    print(f"** Skipped ** {filename}: Empty file")
                    
            else:
                print(f"** Skipped ** {filename}: File type not supported")
                
        except Exception as e:
            print(f"** Skipped ** {filename}: {e}")
    
    print(f"\nProcessed {processed}/{len(files_to_process)} files")
    return documents

def get_document_files(docs_dir):
    """Get all files from directory (filtering happens during processing)"""
    return [f for f in os.listdir(docs_dir) 
            if os.path.isfile(os.path.join(docs_dir, f))]