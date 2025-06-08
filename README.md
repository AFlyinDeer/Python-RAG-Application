PDF RAG (Retrieval-Augmented Generation) System
A comprehensive document question-answering system that processes PDF and DOCX files using ChromaDB vector storage and local LLM inference with Ollama.

🚀 Features
    Multi-format Support: Process both PDF and DOCX documents
    Local LLM Integration: Uses Ollama with Llama 3.1 for privacy-focused inference
    Vector Database: ChromaDB for efficient similarity search and document retrieval
    Incremental Updates: Add new documents without rebuilding the entire database
    Interactive Q&A: Command-line interface for real-time document querying
    Similarity Filtering: Advanced retrieval with configurable similarity thresholds
    Source Attribution: Automatic citation of source documents and page numbers
    Automatic Setup: Database initialization with error handling and status checking

📋 Prerequisites
    Required Software
    Python 3.8+
    Ollama installed and running locally
    Required Python packages (see Installation section)
    Ollama Models
    The system requires these Ollama models to be installed:

bash
# Install the LLM model
ollama pull llama3.1

# Install the embedding model
ollama pull nomic-embed-text

🛠️ Installation
    Clone or download the project files
    Install Python dependencies:
    bash
    pip install langchain langchain-ollama langchain-chroma langchain-community
    pip install pypdf docx2txt chromadb
    Verify Ollama is running:
    bash

# Check if Ollama service is active
ollama list
    Configure paths (optional):
    Edit database.py to change the database directory (DB_DIR)
    Edit db_setup.py to change the documents directory (DOCS_DIR)

📁 Project Structure
RAG/
├── main.py                 # Basic RAG system entry point
├── main_w_db_check.py     # Enhanced version with auto-setup
├── sim_search.py          # Similarity threshold-based retrieval
├── database.py            # Vector database management
├── db_setup.py           # Database initialization and updates
├── file_processing.py    # Document loading and text splitting
├── user_retrieval.py     # Interactive Q&A interface
├── docs/                 # Place your PDF/DOCX files here
└── instance/             # ChromaDB storage (auto-created)

🚀 Quick Start
1. Add Your Documents
Place your PDF and DOCX files in the docs/ directory:

docs/
├── research_paper.pdf
├── manual.docx
└── report.pdf
2. Run the System
Option A: Automatic Setup (Recommended)

bash
python main_w_db_check.py
This version automatically checks for and creates the database if needed.

Option B: Manual Setup

bash
# First, set up the database
python db_setup.py

# Then run the main application
python main.py
Option C: Similarity-Based Retrieval

bash
python sim_search.py
Uses similarity thresholds for more precise document retrieval.

3. Start Asking Questions
PDF RAG System Ready!
Type 'quit' to exit
---------------------

Question: What are the main findings in the research paper?
Answer: Based on the research paper, the main findings include...
(2.3s)

Sources:
  1. research_paper.pdf (p.5) [PDF]
  2. research_paper.pdf (p.12) [PDF]
⚙️ Configuration
Database Settings (database.py)
python
DB_DIR = r"F:\Code\RAGProject\RAG\instance"    # Database storage path
COLLECTION_NAME = "pdf_docs"                    # ChromaDB collection name
EMBEDDING_MODEL = "nomic-embed-text"            # Ollama embedding model
Document Processing (db_setup.py)
python
DOCS_DIR = r"F:\Code\RAGProject\RAG\docs"      # Documents directory
CHUNK_SIZE = 800                                # Text chunk size
OVERLAP = 100                                   # Chunk overlap for context
LLM Settings (main.py, sim_search.py)
python
MODEL_NAME = "llama3.1"        # Ollama model name
MAX_CHUNKS = 5                 # Maximum chunks per query
SIMILARITY_THRESHOLD = 0.7     # Minimum similarity score (sim_search.py)
📚 Usage Examples
Basic Document Queries
Question: Summarize the methodology section
Question: What are the key recommendations?
Question: Explain the technical specifications
Specific Information Retrieval
Question: What is the budget allocation for Q3?
Question: List the safety protocols mentioned
Question: What are the system requirements?
Cross-Document Analysis
Question: Compare the findings between the two reports
Question: What common themes appear across documents?
🔧 Advanced Features
Adding New Documents
The system automatically detects new files:

bash
# Add new files to docs/ directory, then run:
python db_setup.py

# Or use the auto-setup version:
python main_w_db_check.py
Similarity Threshold Tuning
For more precise results, adjust the similarity threshold:

python
# In sim_search.py
run_similarity_search(threshold=0.8)  # Higher = more strict
run_similarity_search(threshold=0.5)  # Lower = more inclusive
Batch Processing
The system processes documents in batches for memory efficiency:

python
# Configurable in db_setup.py
batch_size = 50  # Adjust based on available memory
🐛 Troubleshooting
Common Issues
1. "Database not found" Error

bash
# Solution: Run database setup
python db_setup.py
2. "Ollama model not found" Error

bash
# Solution: Install required models
ollama pull llama3.1
ollama pull nomic-embed-text
3. "No documents found" Error

Check that PDF/DOCX files are in the docs/ directory
Verify file permissions and formats
4. Slow Performance

Reduce MAX_CHUNKS in configuration
Lower num_ctx in LLM settings
Use SSD storage for the database
5. Memory Issues

Reduce CHUNK_SIZE and batch_size
Restart Ollama service
Close other applications
Debug Mode
Enable detailed logging by uncommenting debug lines in database.py:

python
# Debugging
print(f"Loaded {count} documents")
📊 Performance Optimization
Memory Management
Uses garbage collection (gc.collect()) after processing
Processes documents in configurable batches
Efficient text splitting with overlap
Speed Optimization
ChromaDB for fast vector similarity search
Configurable similarity thresholds
Optimized LLM parameters for faster inference
Storage Efficiency
Incremental database updates
Persistent vector storage
Metadata-based file tracking
🔒 Privacy & Security
Fully Local: No data sent to external services
Ollama Integration: Local LLM inference only
Document Privacy: Files processed and stored locally
No API Keys: No external API dependencies
🤝 Contributing
To extend the system:

Add new document formats: Modify file_processing.py
Custom retrievers: Extend BaseRetriever class
Different LLMs: Update model configuration
Enhanced prompts: Modify prompt templates
📄 License
This project is provided as-is for educational and research purposes.

🆘 Support
For issues and questions:

Check the troubleshooting section above
Verify all dependencies are installed correctly
Ensure Ollama is running with required models
Check file paths and permissions
Note: Make sure to adjust the file paths in the configuration files to match your system setup before running the application.

