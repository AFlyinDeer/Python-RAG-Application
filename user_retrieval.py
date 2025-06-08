import time

def ask_question(qa_chain, question):
    """Ask a question and get answer"""
    start_time = time.time()
    
    try:
        result = qa_chain.invoke({"query": question})
        
        query_time = time.time() - start_time
        answer = result["result"]
        sources = result["source_documents"]
        
        print(f"\nAnswer: {answer}")
        print(f"\n({query_time:.1f}s)")
        
        if sources:
            print(f"\nSources:")
            for i, doc in enumerate(sources, 1):
                page = doc.metadata.get('page', '?')
                source_file = doc.metadata.get('source_file', 'Unknown')
                file_type = doc.metadata.get('file_type', '')
                if file_type:
                    print(f"  {i}. {source_file} (p.{page}) [{file_type.upper()}]")
                else:
                    print(f"  {i}. {source_file} (p.{page})")
        
        return answer, sources
        
    except Exception as e:
        print(f"Error: {e}")
        return None, []

def run_interactive(qa_chain):
    """Run interactive Q&A session"""
    print("-" * 21)
    print("PDF RAG System Ready!")
    print("Type 'quit' to exit")
    print("-" * 21)
    
    while True:
        question = input("\nQuestion: ").strip()
        
        if question.lower() == 'quit':
            break
        elif not question:
            continue
        
        ask_question(qa_chain, question)

def quick_query(qa_chain, question):
    """Ask one question and return results"""
    answer, sources = ask_question(qa_chain, question)
    return answer, sources