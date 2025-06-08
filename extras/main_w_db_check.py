import gc
import os
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from database import load_vectorstore, check_database
from user_retrieval import run_interactive

# Configuration
MODEL_NAME = "llama3.1"
MAX_CHUNKS = 3

def create_llm():
    """Create LLM with efficient settings"""
    llm = OllamaLLM(
        model=MODEL_NAME,
        temperature=0.7,
        num_ctx=2048,
        num_predict=256,
        num_thread=2,
        repeat_penalty=1.1,
        top_k=10,
        top_p=0.9
    )
    
    return llm

def setup_qa_chain(vectorstore):
    """Setup QA chain"""
    llm = create_llm()
    
    prompt_template = """Analyze the provided context from multiple sources to answer the question comprehensively. Be concise and helpful, expand to give some extra context. Do not ask if the user needs more information or ask the user questions.

    Context: {context}
    Question: {question}
    Answer:"""
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": MAX_CHUNKS}
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    return qa_chain

def main():
    """Main function to run the RAG system"""
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
        
        vectorstore = load_vectorstore()
        qa_chain = setup_qa_chain(vectorstore)
        
        # Run interactive session
        run_interactive(qa_chain)
        
    except Exception as e:
        print(f"Failed to start: {e}")
    
    finally:
        gc.collect()

if __name__ == "__main__":
    main()