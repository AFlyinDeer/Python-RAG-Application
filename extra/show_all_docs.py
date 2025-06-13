from database import load_vectorstore

def show_all_documents():
    """Print all documents from the vectorstore"""
    try:
        print("Loading vectorstore...")
        vectorstore = load_vectorstore()
        
        print("Getting all documents...")
        all_docs = vectorstore.get(include=['documents', 'metadatas', 'embeddings'])
        
        print("\n" + "="*50)
        print("ALL DOCUMENTS IN COLLECTION")
        print("="*50)
        
        # Print basic info
        num_docs = len(all_docs['documents'])
        print(f"Total documents: {num_docs}")
        
        if num_docs > 0:
            print(f"Embedding dimension: {len(all_docs['embeddings'][0])}")
        
        print("\n" + "-"*50)
        
        # Print each document
        for i in range(num_docs):
            print(f"\nDocument {i+1}:")
            #print(f"Content: {all_docs['documents'][i]}")
            print(f"Metadata: {all_docs['metadatas'][i]}")
            print(f"Embedding (first 5): {all_docs['embeddings'][i]}")
            print("-" * 30)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_all_documents()