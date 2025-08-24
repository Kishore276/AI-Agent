#!/usr/bin/env python3
"""
Multilingual College AI Agent API Server
Flask-based REST API supporting all Indian languages
"""

from flask import Flask, request, jsonify, render_template_string
import pickle
import json
import os
from pathlib import Path
import logging
import pandas as pd
from datetime import datetime

# Import the multilingual agent
try:
    from train_college_ai_agent import CollegeAIAgent, INDIAN_LANGUAGES
    print("✅ Multilingual College AI Agent imported successfully")
except ImportError as e:
    print(f"❌ Error importing agent: {e}")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global agent instance
agent = None

def initialize_agent():
    """Initialize the multilingual agent"""
    global agent
    
    try:
        logger.info("🤖 Initializing Multilingual College AI Agent...")
        
        # Try to load existing model first
        model_path = "multilingual_college_ai.pkl"
        if os.path.exists(model_path):
            agent = CollegeAIAgent(enable_multilingual=True)
            if agent.load_model(model_path):
                logger.info("✅ Loaded existing multilingual model")
                return True
        
        # Create new agent if no model exists
        agent = CollegeAIAgent(enable_multilingual=True)
        
        # Generate multilingual data if not available
        if not agent.multilingual_qa_pairs:
            logger.info("🌐 Generating multilingual data...")
            agent.generate_multilingual_data()
            agent.create_embeddings()
            agent.save_model(model_path)
            logger.info("✅ Multilingual model created and saved")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error initializing agent: {e}")
        return False

@app.route('/')
def home():
    """Home page with API documentation"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌐 Multilingual College AI Agent API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #2c3e50; text-align: center; }
            h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { background: #3498db; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
            .language { display: inline-block; margin: 5px; padding: 5px 10px; background: #e74c3c; color: white; border-radius: 3px; }
            code { background: #2c3e50; color: white; padding: 2px 5px; border-radius: 3px; }
            .example { background: #f8f9fa; border-left: 4px solid #28a745; padding: 15px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌐 Multilingual College AI Agent API</h1>
            
            <h2>📋 API Endpoints</h2>
            
            <div class="endpoint">
                <span class="method">POST</span> <code>/query</code>
                <p>Query the AI agent in any supported Indian language</p>
                <div class="example">
                    <strong>Request:</strong><br>
                    <code>{"question": "आईआईटी बॉम्बे में फीस कितनी है?", "language": "hi", "top_k": 3}</code><br><br>
                    <strong>Response:</strong><br>
                    <code>{"query": "...", "results": [...], "language": "hi", "total_results": 3}</code>
                </div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <code>/languages</code>
                <p>Get list of all supported languages</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <code>/health</code>
                <p>Check API health and model status</p>
            </div>
            
            <h2>🌍 Supported Languages</h2>
            <div>
                {% for lang in languages %}
                <span class="language">{{ lang.native }} ({{ lang.name }})</span>
                {% endfor %}
            </div>
            
            <h2>💡 Example Usage</h2>
            <div class="example">
                <strong>Hindi Query:</strong><br>
                <code>curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"question": "आईआईटी में प्रवेश कैसे लें?"}'</code><br><br>
                
                <strong>Bengali Query:</strong><br>
                <code>curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"question": "আইআইটিতে ভর্তি কীভাবে হয়?"}'</code><br><br>
                
                <strong>English Query:</strong><br>
                <code>curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"question": "How to get admission in IIT?"}'</code>
            </div>
        </div>
    </body>
    </html>
    """
    
    languages = [
        {'native': info['native'], 'name': info['name']} 
        for info in INDIAN_LANGUAGES.values()
    ]
    
    return render_template_string(html_template, languages=languages)

@app.route('/query', methods=['POST'])
def query_agent():
    """Handle multilingual queries"""
    try:
        if not agent:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        question = data.get('question', '').strip()
        target_language = data.get('language')
        top_k = data.get('top_k', 5)
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        logger.info(f"🔍 Query received: {question[:50]}...")
        
        # Query the agent
        results = agent.query_agent(question, top_k=top_k, target_language=target_language)
        
        # Prepare response
        response = {
            'query': question,
            'results': results,
            'total_results': len(results),
            'language': results[0].get('language', 'en') if results else 'en',
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Query processed: {len(results)} results returned")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Query error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    try:
        if agent and agent.translator:
            languages = agent.get_supported_languages()
        else:
            languages = [{'code': code, 'name': info['name'], 'native': info['native']} 
                        for code, info in INDIAN_LANGUAGES.items()]
        
        return jsonify({
            'supported_languages': languages,
            'total_languages': len(languages),
            'multilingual_enabled': agent.enable_multilingual if agent else False
        })
        
    except Exception as e:
        logger.error(f"❌ Languages error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if not agent:
            return jsonify({
                'status': 'unhealthy',
                'error': 'Agent not initialized'
            }), 500
        
        # Calculate statistics
        total_colleges = len(agent.colleges_data)
        total_qa_pairs = len(agent.qa_pairs)
        
        if agent.multilingual_qa_pairs:
            total_multilingual_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
            supported_languages = len(agent.multilingual_qa_pairs)
        else:
            total_multilingual_pairs = total_qa_pairs
            supported_languages = 1
        
        return jsonify({
            'status': 'healthy',
            'agent_initialized': True,
            'multilingual_enabled': agent.enable_multilingual,
            'total_colleges': total_colleges,
            'total_qa_pairs': total_qa_pairs,
            'total_multilingual_pairs': total_multilingual_pairs,
            'supported_languages': supported_languages,
            'model_loaded': agent.embeddings is not None,
            'translation_available': agent.translator is not None
        })
        
    except Exception as e:
        logger.error(f"❌ Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function to start the API server"""
    print("🌐 Starting Multilingual College AI Agent API Server")
    print("=" * 60)
    
    # Initialize the agent
    if not initialize_agent():
        print("❌ Failed to initialize agent. Exiting.")
        return
    
    print("✅ Agent initialized successfully")
    print(f"🌐 Supporting {len(INDIAN_LANGUAGES)} languages")
    print(f"📚 {len(agent.colleges_data)} colleges in database")
    
    if agent.multilingual_qa_pairs:
        total_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
        print(f"💬 {total_pairs:,} multilingual Q&A pairs")
    else:
        print(f"💬 {len(agent.qa_pairs):,} English Q&A pairs")
    
    print("\n🚀 Starting Flask server...")
    print("📡 API will be available at: http://localhost:5000")
    print("📖 API documentation at: http://localhost:5000")
    print("\n🔍 Example queries:")
    print("   Hindi: आईआईटी में फीस कितनी है?")
    print("   Bengali: আইআইটিতে ভর্তি কীভাবে হয়?")
    print("   English: What is the fee at IIT?")
    
    # Start the server
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
