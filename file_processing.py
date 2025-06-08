import os
import gc
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import docx2txt

def get_processed_files(vectorstore):
    """Get list of files already in the database"""
    try:
        all_docs = vectorstore.get(include=['metadatas'])
        processed_files = set()
        
        for metadata in all_docs['metadatas']:
            if metadata and 'source_file' in metadata:
                processed_files.add(metadata['source_file'])
        
        return processed_files
    except Exception:
        return set()

def load_docx(file_path):
    """Load and extract text from a DOCX file"""
    try:
        content = docx2txt.process(file_path)
        return content.strip() if content else ""
    except Exception as e:
        print(f"Error loading DOCX {file_path}: {e}")
        return ""

def load_and_split_documents(docs_dir, files_to_process, chunk_size=800, overlap=100):
    """Load and split specified PDF and DOCX files"""
    if not files_to_process:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    all_documents = []
    processed_count = 0
    skipped_files = []
    
    for file_name in files_to_process:
        print(f"Processing: {file_name}")
        
        file_path = os.path.join(docs_dir, file_name)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        try:
            if file_ext == '.pdf':
                # Handle PDF files
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                splits = text_splitter.split_documents(documents)
                
                # Add metadata for PDFs
                for doc in splits:
                    doc.metadata = {
                        'source_file': file_name,
                        'page': doc.metadata.get('page', 0),
                        'file_type': 'pdf'
                    }
                
                all_documents.extend(splits)
                processed_count += 1
                del loader, documents
                
            elif file_ext == '.docx':
                # Handle DOCX files
                content = load_docx(file_path)
                if content:
                    # Create a Document object for the DOCX content
                    doc = Document(page_content=content, metadata={'source': file_path})
                    splits = text_splitter.split_documents([doc])
                    
                    # Add metadata for DOCX files
                    for i, split_doc in enumerate(splits):
                        split_doc.metadata = {
                            'source_file': file_name,
                            'page': i + 1,  # Use chunk number as "page"
                            'file_type': 'docx'
                        }
                    
                    all_documents.extend(splits)
                    processed_count += 1
                else:
                    print(f"** Skipped ** {file_name}: Empty or corrupted DOCX")
                    skipped_files.append(file_name)
            
            else:
                print(f"** Skipped ** {file_name}: Unsupported file type ({file_ext})")
                skipped_files.append(file_name)
                continue
        
        except Exception as e:
            print(f"** Skipped ** {file_name}: {str(e)}")
            skipped_files.append(file_name)
            continue
        
        gc.collect()
    
    # Summary
    print(f"\n** Successfully processed: {processed_count}/{len(files_to_process)} files **")
    if skipped_files:
        print(f"** Skipped files: {', '.join(skipped_files)} **")
    
    return all_documents

def get_document_files(docs_dir):
    """Get list of PDF and DOCX files in directory"""
    supported_extensions = ['.pdf', '.docx']
    files = []
    
    for filename in os.listdir(docs_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in supported_extensions:
            files.append(filename)
    
    return files