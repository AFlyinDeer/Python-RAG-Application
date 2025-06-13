import gc
import numpy as np
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from typing import List
from database import load_vectorstore, check_database
from user_retrieval import run_interactive
from config import MODEL_NAME, SIMILARITY_THRESHOLD, MAX_CHUNKS, LLM_CONFIG, PROMPT_TEMPLATE

def create_llm():
    """Create LLM with configuration from config.py"""
    llm = OllamaLLM(
        model=MODEL_NAME,
        **LLM_CONFIG  # Unpack the config dictionary
    )
    return llm

class SimilarityRetriever(BaseRetriever):
    """Similarity threshold-based retriever"""
    
    vectorstore: object
    threshold: float = SIMILARITY_THRESHOLD
    max_chunks: int = MAX_CHUNKS
    
    class Config:
        arbitrary_types_allowed = True
    
    def _get_relevant_documents(
        self, 
        query: str, 
        *, 
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Get documents above similarity threshold"""
        
        # Get more chunks with similarity scores
        results = self.vectorstore.similarity_search_with_score(
            query, 
            k=self.max_chunks
        )
        
        # Filter by threshold (Chroma returns cosine distance: lower = more similar)
        filtered_docs = []
        
        for doc, score in results:
            # Convert distance to similarity (score is cosine distance)
            similarity = 1 - score
            
            if similarity >= self.threshold:
                filtered_docs.append(doc)
        
        # If no docs meet threshold, return the best 2-3 to avoid empty results
        if not filtered_docs and results:
            filtered_docs = [doc for doc, _ in results[:3]]
        
        # Debugging
        #print(f"Found {len(filtered_docs)} relevant chunks (threshold: {self.threshold})")
        
        return filtered_docs

def setup_similarity_qa_chain(vectorstore, threshold=SIMILARITY_THRESHOLD):
    """Setup QA chain with similarity threshold-based retrieval"""
    llm = create_llm()
    
    prompt_template = PROMPT_TEMPLATE.format(threshold=threshold)
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Create similarity threshold-based retriever
    retriever = SimilarityRetriever(
        vectorstore=vectorstore, 
        threshold=threshold, 
        max_chunks=MAX_CHUNKS
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    return qa_chain

def run_similarity_search(threshold=SIMILARITY_THRESHOLD):
    """Run the similarity-based RAG system"""
    try:
        # Check if database exists before proceeding
        exists, status = check_database()
        
        # Debugging
        # print(f"Database status: {status}")
        
        if not exists:
            print("\nDatabase not found. Running setup...")
            
            # Import and run setup function directly
            try:
                from db_setup import setup_database
                if setup_database():
                    print("Setup completed successfully!")
                    
                    # Check again after setup
                    exists, status = check_database()
                    if not exists:
                        print("Database still not available after setup. Please check db_setup.py")
                        return
                else:
                    print("Setup failed. Please run 'python db_setup.py' manually.")
                    return
                    
            except Exception as setup_error:
                print(f"Setup failed: {setup_error}")
                print("Please run 'python db_setup.py' manually.")
                return
        
        print(f"Loading vectorstore...")
        vectorstore = load_vectorstore()
        # Debugging
        #print(f"Setting up similarity-based QA (threshold: {threshold})...")
        qa_chain = setup_similarity_qa_chain(vectorstore, threshold)
        
        # Debugging
        #print(f"Similarity RAG System Ready! (min similarity: {threshold})")
        
        # Run interactive session
        run_interactive(qa_chain)
        
    except Exception as e:
        print(f"Failed to start similarity search: {e}")
    
    finally:
        gc.collect()

if __name__ == "__main__":
    run_similarity_search()  