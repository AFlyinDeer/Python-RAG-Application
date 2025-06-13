from flask import Flask, request, jsonify
from flask_cors import CORS
from sim_search import run_similarity_search, setup_similarity_qa_chain, SIMILARITY_THRESHOLD
from database import load_vectorstore, check_database
from db_setup import setup_database


app = Flask(__name__)
CORS(app)

# Initialize on startup
vectorstore = load_vectorstore()
qa_chain = setup_similarity_qa_chain(vectorstore, SIMILARITY_THRESHOLD)

def initialize_system():
    """Initialize the RAG system"""
    global qa_chain, vectorstore
    
    try:
        # Check if database exists
        exists, status = check_database()
        
        if not exists:
            if not setup_database():
                return False, "Database setup failed"
        
        # Load vectorstore and setup QA chain
        vectorstore = load_vectorstore()
        qa_chain = setup_similarity_qa_chain(vectorstore, SIMILARITY_THRESHOLD)
        
        return True, "System initialized successfully"
        
    except Exception as e:
        return False, f"Initialization failed: {str(e)}"

# Search
@app.route('/api/search', methods=['POST'])
def search():
    question = request.json['question']
    result = qa_chain.invoke({"query": question})
    return jsonify({
        "answer": result["result"],
        "sources": [f"{doc.metadata.get('source_file')} (p.{doc.metadata.get('page', '?')})" 
                   for doc in result["source_documents"]]
    })

# Health
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "system_ready": qa_chain is not None
    })

# Status
@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    exists, status = check_database()
    return jsonify({
        "database_exists": exists,
        "database_status": status,
        "system_ready": qa_chain is not None
    }) 

# Initialize
@app.route('/api/initialize', methods=['POST'])
def initialize():
    """Initialize or reinitialize the system"""
    success, message = initialize_system()
    
    if success:
        return jsonify({
            "success": True,
            "message": message
        })
    else:
        return jsonify({
            "success": False,
            "error": message
        }), 500  

app.run(debug=True, port=5000)