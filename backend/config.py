# Docs

DOCS_DIR = r"F:\Code\RAGProject\RAG\documents"
DB_DIR = r"F:\Code\RAGProject\RAG\instance"

COLLECTION_NAME = "all_docs"
CHUNK_SIZE = 500
OVERLAP = 100
BATCH_SIZE = 50

# AI

#MODEL_NAME = "llama3.1"
#MODEL_NAME = "llama3.2:1b-instruct-q4_0"
MODEL_NAME = "llama3.2:3b-instruct-q4_0"
EMBEDDING_MODEL = "all-minilm"
#EMBEDDING_MODEL = "nomic-embed-text"
#EMBEDDING_MODEL = "mxbai-embed-large"

SIMILARITY_THRESHOLD = 0.3
MAX_CHUNKS = 5  


# LLM

LLM_FAST_CONFIG = {
    "temperature": 0.7,     # Controls randomness/creativity in responses: Range: 0.0 (deterministic) to 2.0 (very random)
    "num_ctx": 512,         # Context window size - how many tokens the model can "remember"
    "num_predict": 500,     # Maximum number of tokens the model will generate in a single response: Higher values allow longer responses but use more resources 
    "num_threads": 4,       # Number of CPU threads used for inference (Leave 4 free)
    "repeat_penalty": 1.1,  # Reduces repetitive text generation
    "top_k": 3,             # Limits vocabulary to the top K most likely next tokens
    "top_p": 0.7            # Nucleus sampling - considers tokens until cumulative probability reaches this threshold
}

LLM_BALANCED_CONFIG = {
    "temperature": 0.7,
    "num_ctx": 1024,        
    "num_predict": 750,     
    "num_threads": 4,       
    "repeat_penalty": 1.1,
    "top_k": 5,            
    "top_p": 0.8           
}

LLM_HEAVY_CONFIG = {
    "temperature": 0.7,
    "num_ctx": 2048,        
    "num_predict": 1000,     
    "num_threads": 4,       
    "repeat_penalty": 1.1,
    "top_k": 10,            
    "top_p": 0.9           
}

LLM_CONFIG = LLM_FAST_CONFIG
# LLM_CONFIG = LLM_BALANCED_CONFIG
# LLM_CONFIG = LLM_HEAVY_CONFIG


PROMPT_TEMPLATE = """Analyze the provided context from multiple sources to answer the question. Provide a complete, well-structured answer in 2-3 paragraphs maximum. Be concise but thorough, and ensure you finish your complete thought.

Keep your response around 400 charcters if you can.

Note: Only highly relevant context (similarity >= {threshold}) is provided below.

Context: {{context}}
Question: {{question}}

Complete Answer:"""


# Embedding

HNSW_FAST_CONFIG = {
    "hnsw:space": "cosine",           
}

HNSW_BALANCED_CONFIG = {
    "hnsw:space": "cosine",           # Distance metric
    "hnsw:construction_ef": 200,      # Build quality (higher = better, slower)
    "hnsw:M": 16,                     # Max connections per node
    "hnsw:search_ef": 100,            # Search quality (higher = better, slower)
    "hnsw:num_threads": 12,           # Use your CPU cores
    "hnsw:sync_threshold": 1000       # Disk write threshold
}

# HNSW_CONFIG = HNSW_FAST_CONFIG
HNSW_CONFIG = HNSW_BALANCED_CONFIG