#!/usr/bin/env python3
"""
Voice & Chat College AI Assistant
Flask web application with voice input/output and text chat
Integrated with trained ML model for college information
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import pickle
import tempfile
import threading
from pathlib import Path
from datetime import datetime
import base64
import io

# Voice processing libraries
try:
    import speech_recognition as sr
    import pyttsx3
    from pydub import AudioSegment
    import wave
    VOICE_AVAILABLE = True
    print("✅ Voice libraries available")
except ImportError as e:
    print(f"⚠️  Voice libraries not available: {e}")
    print("📦 Install with: pip install SpeechRecognition pyttsx3 pydub")
    VOICE_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'college_ai_voice_chat_2024'

class VoiceChatAgent:
    """Voice and Chat enabled College AI Agent"""
    
    def __init__(self, model_path="college_ai_rtx2050_trained.pkl"):
        self.model_path = model_path
        self.agent = None
        self.conversation_history = []
        
        # Initialize voice components
        if VOICE_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.tts_engine = pyttsx3.init()
            self.setup_voice()
        
        # Load trained model
        self.load_model()
        
        print("🎤 Voice & Chat Agent initialized")
    
    def setup_voice(self):
        """Setup text-to-speech engine"""
        if not VOICE_AVAILABLE:
            return
        
        try:
            # Configure TTS
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a female voice or use first available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
            
            print("🔊 Text-to-Speech configured")
        except Exception as e:
            print(f"⚠️  TTS setup error: {e}")
    
    def load_model(self):
        """Load the trained college AI model"""
        try:
            if Path(self.model_path).exists():
                # Try to load using the original agent class
                try:
                    from train_college_ai_agent import CollegeAIAgent
                    self.agent = CollegeAIAgent(enable_multilingual=True)
                    success = self.agent.load_model(self.model_path)
                    if success:
                        print(f"✅ ML model loaded: {len(self.agent.colleges_data)} colleges")
                        return True
                except Exception:
                    pass
                
                # Fallback: Load as pickle
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                class SimpleAgent:
                    def __init__(self, data):
                        self.colleges_data = data.get('colleges_data', {})
                        self.qa_pairs = data.get('qa_pairs', [])
                        self.embeddings = data.get('embeddings')
                    
                    def query_agent(self, question, top_k=5, target_language=None):
                        # Simple keyword-based search
                        results = []
                        question_lower = question.lower()
                        
                        for qa in self.qa_pairs[:200]:  # Limit for performance
                            qa_text = f"{qa.get('question', '')} {qa.get('answer', '')}".lower()
                            score = 0
                            
                            for word in question_lower.split():
                                if len(word) > 2 and word in qa_text:
                                    score += 1
                            
                            if score > 0:
                                results.append({
                                    'college': qa.get('college', 'Unknown'),
                                    'category': qa.get('category', 'general'),
                                    'question': qa.get('question', ''),
                                    'answer': qa.get('answer', ''),
                                    'confidence': min(score * 15, 95)
                                })
                        
                        return sorted(results, key=lambda x: x['confidence'], reverse=True)[:top_k]
                
                self.agent = SimpleAgent(model_data)
                print(f"✅ Model loaded: {len(self.agent.colleges_data)} colleges")
                return True
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def process_voice_input(self, audio_data):
        """Process voice input and return text"""
        if not VOICE_AVAILABLE:
            return "Voice processing not available"
        
        try:
            # Convert audio data to text
            audio_file = sr.AudioFile(audio_data)
            with audio_file as source:
                audio = self.recognizer.record(source)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            print(f"🎤 Voice input: {text}")
            return text
            
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio"
        except sr.RequestError as e:
            return f"Speech recognition error: {e}"
        except Exception as e:
            return f"Voice processing error: {e}"
    
    def generate_voice_response(self, text):
        """Generate voice response from text"""
        if not VOICE_AVAILABLE:
            return None
        
        try:
            # Create temporary file for audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_path = temp_file.name
            temp_file.close()
            
            # Generate speech
            self.tts_engine.save_to_file(text, temp_path)
            self.tts_engine.runAndWait()
            
            return temp_path
            
        except Exception as e:
            print(f"❌ Voice generation error: {e}")
            return None
    
    def process_query(self, question, input_type="text"):
        """Process user query and return response"""
        if not self.agent:
            return {
                'answer': "Sorry, the AI model is not available. Please ensure the model is trained.",
                'confidence': 0,
                'college': 'System',
                'input_type': input_type,
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Query the ML model
            results = self.agent.query_agent(question, top_k=3)
            
            if results:
                best_result = results[0]
                
                # Format response
                response = {
                    'question': question,
                    'answer': best_result['answer'],
                    'confidence': best_result.get('confidence', 0),
                    'college': best_result.get('college', 'Unknown'),
                    'category': best_result.get('category', 'general'),
                    'input_type': input_type,
                    'timestamp': datetime.now().isoformat(),
                    'alternatives': []
                }
                
                # Add alternative answers
                for result in results[1:]:
                    response['alternatives'].append({
                        'college': result.get('college', 'Unknown'),
                        'answer': result['answer'][:100] + "...",
                        'confidence': result.get('confidence', 0)
                    })
                
                # Add to conversation history
                self.conversation_history.append({
                    'user': question,
                    'assistant': best_result['answer'],
                    'timestamp': datetime.now().isoformat(),
                    'input_type': input_type
                })
                
                return response
            else:
                return {
                    'question': question,
                    'answer': "I couldn't find specific information about that. Could you please rephrase your question or ask about college fees, admissions, placements, or facilities?",
                    'confidence': 0,
                    'college': 'Assistant',
                    'category': 'help',
                    'input_type': input_type,
                    'timestamp': datetime.now().isoformat(),
                    'alternatives': []
                }
                
        except Exception as e:
            print(f"❌ Query processing error: {e}")
            return {
                'question': question,
                'answer': f"Sorry, there was an error processing your question: {str(e)}",
                'confidence': 0,
                'college': 'System',
                'input_type': input_type,
                'timestamp': datetime.now().isoformat(),
                'alternatives': []
            }
    
    def get_conversation_history(self):
        """Get conversation history"""
        return self.conversation_history[-10:]  # Last 10 conversations
    
    def get_stats(self):
        """Get agent statistics"""
        return {
            'total_colleges': len(self.agent.colleges_data) if self.agent else 0,
            'total_qa_pairs': len(self.agent.qa_pairs) if self.agent else 0,
            'conversations': len(self.conversation_history),
            'voice_enabled': VOICE_AVAILABLE,
            'model_loaded': self.agent is not None
        }

# Initialize the agent
voice_agent = VoiceChatAgent()

@app.route('/')
def home():
    """Main page"""
    stats = voice_agent.get_stats()
    return render_template('voice_chat.html', stats=stats)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle text chat"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Process the query
        response = voice_agent.process_query(question, input_type="text")
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice', methods=['POST'])
def voice_input():
    """Handle voice input"""
    if not VOICE_AVAILABLE:
        return jsonify({'error': 'Voice processing not available'}), 400
    
    try:
        # Get audio file from request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Save temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio_file.save(temp_file.name)
        
        # Process voice input
        question = voice_agent.process_voice_input(temp_file.name)
        
        # Clean up
        os.unlink(temp_file.name)
        
        if "error" in question.lower() or "sorry" in question.lower():
            return jsonify({'error': question}), 400
        
        # Process the query
        response = voice_agent.process_query(question, input_type="voice")
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice_response', methods=['POST'])
def voice_response():
    """Generate voice response"""
    if not VOICE_AVAILABLE:
        return jsonify({'error': 'Voice generation not available'}), 400
    
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate voice response
        audio_path = voice_agent.generate_voice_response(text)
        
        if audio_path and os.path.exists(audio_path):
            return send_file(audio_path, as_attachment=True, download_name='response.wav')
        else:
            return jsonify({'error': 'Voice generation failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get conversation history"""
    try:
        history = voice_agent.get_conversation_history()
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get agent statistics"""
    try:
        stats = voice_agent.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Voice & Chat College AI Assistant")
    print("=" * 60)
    
    # Check if model exists
    if not Path("college_ai_rtx2050_trained.pkl").exists():
        print("⚠️  Model file not found: college_ai_rtx2050_trained.pkl")
        print("📋 Please train the model first:")
        print("   python train_rtx2050_gpu.py")
    
    print(f"🌐 Web app will be available at: http://localhost:5000")
    print(f"🎤 Voice input: {'✅ Available' if VOICE_AVAILABLE else '❌ Not available'}")
    print(f"🔊 Voice output: {'✅ Available' if VOICE_AVAILABLE else '❌ Not available'}")
    print(f"💬 Text chat: ✅ Available")
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
