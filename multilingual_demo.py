#!/usr/bin/env python3
"""
Multilingual College AI Agent Demo
Demonstrates querying in multiple Indian languages
"""

import sys
import json
from pathlib import Path

# Import the multilingual agent
try:
    from train_college_ai_agent import CollegeAIAgent, INDIAN_LANGUAGES
    print("✅ Multilingual College AI Agent imported successfully")
except ImportError as e:
    print(f"❌ Error importing agent: {e}")
    print("📦 Please ensure all requirements are installed:")
    print("   python install_multilingual_requirements.py")
    sys.exit(1)

def display_languages():
    """Display all supported languages"""
    print("🌐 Supported Languages:")
    print("-" * 50)
    
    for i, (code, info) in enumerate(INDIAN_LANGUAGES.items(), 1):
        print(f"   {i:2d}. {info['native']} ({info['name']}) - {code}")
    
    print(f"\nTotal: {len(INDIAN_LANGUAGES)} languages supported")

def demo_multilingual_queries():
    """Demonstrate queries in different languages"""
    
    # Sample queries in different Indian languages
    demo_queries = [
        {
            "language": "English",
            "code": "en",
            "queries": [
                "What is the fee structure at IIT Bombay?",
                "Which companies visit for placements?",
                "What are the admission requirements?"
            ]
        },
        {
            "language": "Hindi",
            "code": "hi", 
            "queries": [
                "आईआईटी बॉम्बे में फीस कितनी है?",
                "प्लेसमेंट के लिए कौन सी कंपनियां आती हैं?",
                "प्रवेश की आवश्यकताएं क्या हैं?"
            ]
        },
        {
            "language": "Bengali",
            "code": "bn",
            "queries": [
                "আইআইটি বোম্বেতে ফি কত?",
                "প্লেসমেন্টের জন্য কোন কোম্পানিগুলি আসে?",
                "ভর্তির প্রয়োজনীয়তা কী?"
            ]
        },
        {
            "language": "Telugu",
            "code": "te",
            "queries": [
                "ఐఐటి బాంబేలో ఫీజు ఎంత?",
                "ప్లేస్‌మెంట్‌ల కోసం ఏ కంపెనీలు వస్తాయి?",
                "అడ్మిషన్ అవసరాలు ఏమిటి?"
            ]
        },
        {
            "language": "Tamil",
            "code": "ta",
            "queries": [
                "ஐஐடி பம்பாயில் கட்டணம் எவ்வளவு?",
                "வேலைவாய்ப்புக்காக எந்த நிறுவனங்கள் வருகின்றன?",
                "சேர்க்கை தேவைகள் என்ன?"
            ]
        },
        {
            "language": "Gujarati",
            "code": "gu",
            "queries": [
                "IIT બોમ્બેમાં ફી કેટલી છે?",
                "પ્લેસમેન્ટ માટે કઈ કંપનીઓ આવે છે?",
                "પ્રવેશની આવશ્યકતાઓ શું છે?"
            ]
        }
    ]
    
    return demo_queries

def interactive_demo():
    """Run interactive multilingual demo"""
    print("🚀 Multilingual College AI Agent Demo")
    print("=" * 60)
    
    # Initialize the agent
    print("🤖 Initializing Multilingual AI Agent...")
    try:
        agent = CollegeAIAgent(enable_multilingual=True)
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Display supported languages
    display_languages()
    
    # Check if multilingual data is available
    if not agent.multilingual_qa_pairs:
        print("\n⚠️  Multilingual data not found. Generating now...")
        print("🔄 This may take several minutes...")
        try:
            agent.generate_multilingual_data()
            agent.create_embeddings()
            agent.save_model("multilingual_college_ai.pkl")
            print("✅ Multilingual data generated and saved")
        except Exception as e:
            print(f"❌ Error generating multilingual data: {e}")
            print("🔤 Falling back to English-only mode")
    
    # Demo queries
    print("\n🎯 Running Multilingual Query Demonstrations:")
    print("-" * 60)
    
    demo_queries = demo_multilingual_queries()
    
    for lang_demo in demo_queries:
        language = lang_demo["language"]
        code = lang_demo["code"]
        queries = lang_demo["queries"]
        
        print(f"\n🌐 {language} ({code}) Queries:")
        print("-" * 30)
        
        for i, query in enumerate(queries, 1):
            print(f"\n❓ Query {i}: {query}")
            
            try:
                results = agent.query_agent(query, top_k=2, target_language=code)
                
                if results:
                    best_result = results[0]
                    print(f"🎯 Best Answer ({best_result['confidence']:.1f}% confidence):")
                    print(f"   🏫 College: {best_result['college']}")
                    print(f"   💡 Answer: {best_result['answer'][:150]}...")
                    
                    if best_result.get('translated'):
                        print(f"   🔄 Translated from English")
                    
                    if len(results) > 1:
                        print(f"   📚 {len(results)-1} more results available")
                else:
                    print("❌ No relevant answers found")
                    
            except Exception as e:
                print(f"❌ Error processing query: {e}")
    
    # Interactive mode
    print(f"\n🎮 Interactive Mode:")
    print("=" * 30)
    print("Ask questions in any supported language!")
    print("Type 'quit' to exit, 'languages' to see supported languages")
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if query.lower() == 'languages':
                display_languages()
                continue
            
            if not query:
                continue
            
            print("🔍 Processing your query...")
            results = agent.query_agent(query, top_k=3)
            
            if results:
                best_result = results[0]
                detected_lang = best_result.get('language', 'en')
                lang_name = INDIAN_LANGUAGES.get(detected_lang, {}).get('name', 'Unknown')
                
                print(f"\n🎯 Best Answer ({best_result['confidence']:.1f}% confidence):")
                print(f"🌐 Detected Language: {lang_name}")
                print(f"🏫 College: {best_result['college']}")
                print(f"📝 Category: {best_result['category']}")
                print(f"💡 Answer: {best_result['answer']}")
                
                if best_result.get('translated'):
                    print(f"🔄 Answer translated to your language")
                
                if len(results) > 1:
                    print(f"\n📚 Other relevant answers:")
                    for i, result in enumerate(results[1:], 2):
                        print(f"   {i}. {result['college']}: {result['answer'][:100]}...")
            else:
                print("❌ No relevant answers found")
                print("💡 Try rephrasing your question or ask about:")
                print("   - College fees and costs")
                print("   - Admission process and requirements") 
                print("   - Placement statistics and companies")
                print("   - College facilities and infrastructure")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    try:
        interactive_demo()
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("📋 Please check that all requirements are installed:")
        print("   python install_multilingual_requirements.py")

if __name__ == "__main__":
    main()
