from langchain_ollama import OllamaEmbeddings

class DebugOllamaEmbeddings(OllamaEmbeddings):
    """OllamaEmbeddings with debugging for embedding vectors"""
    
    def embed_documents(self, texts):
        """Override to print embeddings"""
        embeddings = super().embed_documents(texts)
        
        # Print the embeddings
        for i, embedding in enumerate(embeddings):
            print(f"Embedding {i+1}: {embedding[:5]}...{embedding[-5:]} (shape: {len(embedding)})")
        
        return embeddings
    
    def embed_query(self, text):
        """Override to print query embedding"""
        embedding = super().embed_query(text)
        print(f"Query embedding: {embedding[:5]}...{embedding[-5:]} (shape: {len(embedding)})")
        return embedding