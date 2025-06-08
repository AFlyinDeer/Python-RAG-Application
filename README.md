# PDF RAG (Retrieval-Augmented Generation) System
A comprehensive document question-answering system that processes PDF and DOCX files using ChromaDB vector storage and local LLM inference with Ollama.

# 🚀 Features
Multi-format Support: Process both PDF and DOCX documents\
Local LLM Integration: Uses Ollama with Llama 3.1 for privacy-focused inference\
Vector Database: ChromaDB for efficient similarity search and document retrieval\
Incremental Updates: Add new documents without rebuilding the entire database\
Interactive Q&A: Command-line interface for real-time document querying\
Similarity Filtering: Advanced retrieval with configurable similarity thresholds\
Source Attribution: Automatic citation of source documents and page numbers\
Automatic Setup: Database initialization with error handling and status checking

# 📋 Prerequisites
Required Software\
Python 3.8+\
Ollama installed and running locally\
Required Python packages (see Installation section)\
Ollama Models\
The system requires these Ollama models to be installed:

llama3.1\
nomic-embed-text
# Install the LLM model
ollama pull llama3.1

# Install the embedding model
ollama pull nomic-embed-text

# 🛠️ Installation
Clone or download the project files\
Install Python dependencies:\
In a virtual environment run:

pip install -r requirements.txt

# Check if Ollama service is active
ollama list

# 📁 Project Structure
RAG/\
├── sim_search.py          # Similarity threshold-based retrieval\
├── database.py            # Vector database management\
├── db_setup.py           # Database initialization and updates\
├── file_processing.py    # Document loading and text splitting\
├── user_retrieval.py     # Interactive Q&A interface\
├── debug_embeddings.py      # Print the first and last 5 embeded vector points for each chunk\
├── documents/                 # Place your PDF/DOCX files here\
└── instance/             # ChromaDB storage (auto-created)

# 🚀 Quick Start
1. Add Your Documents\
Place your PDF and DOCX files in the documents/ directory:

documents/\
├── research_paper.pdf\
├── manual.docx\
└── report.pdf

# First, set up the database
python db_setup.py

# Then run the main application
python sim_search.py

# ⚙️ Configuration
Database Settings (database.py)\
python\
DB_DIR = r"F:\Code\RAGProject\RAG\instance"    # Database storage path\
COLLECTION_NAME = "all_docs"                    # ChromaDB collection name\
EMBEDDING_MODEL = "nomic-embed-text"            # Ollama embedding model\
Document Processing (db_setup.py)
python\
DOCS_DIR = r"F:\Code\RAGProject\RAG\docs"      # Documents directory\
CHUNK_SIZE = 800                                # Text chunk size\
OVERLAP = 100                                   # Chunk overlap for context\
LLM Settings (main.py, sim_search.py)\
python\
MODEL_NAME = "llama3.1"        # Ollama model name\
MAX_CHUNKS = 5                 # Maximum chunks per query\
SIMILARITY_THRESHOLD = 0.7     # Minimum similarity score (sim_search.py)\

# 🔧 Advanced Features
Adding New Documents\
The system automatically detects new files:

bash
# Add new files to docs/ directory, then run:
python db_setup.py

# Or use the auto-setup version:
python main_w_db_check.py\
Similarity Threshold Tuning\
For more precise results, adjust the similarity threshold:

python
# In sim_search.py
run_similarity_search(threshold=0.8)  # Higher = more strict\
run_similarity_search(threshold=0.5)  # Lower = more inclusive\
Batch Processing\
The system processes documents in batches for memory efficienc

# 📊 Performance Optimization
Memory Management\
Uses garbage collection (gc.collect()) after processing\
Processes documents in configurable batches\
Efficient text splitting with overlap\
Speed Optimization\
ChromaDB for fast vector similarity search\
Configurable similarity thresholds\
Optimized LLM parameters for faster inference\
Storage Efficiency\
Incremental database updates\
Persistent vector storage\
Metadata-based file tracking

# 🔒 Privacy & Security
Fully Local: No data sent to external services\
Ollama Integration: Local LLM inference only\
Document Privacy: Files processed and stored locally\
No API Keys: No external API dependencies\

# 📄 License
This project is provided as-is for educational and research purposes.

# 🆘 Support
For issues and questions:

Check the troubleshooting section above\
Verify all dependencies are installed correctly\
Ensure Ollama is running with required models\
Check file paths and permissions\
Note: Make sure to adjust the file paths in the configuration files to match your system setup before running the application.

