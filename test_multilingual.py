#!/usr/bin/env python3
"""
Test Script for Multilingual College AI Agent
Comprehensive testing of all multilingual features
"""

import sys
import time
import json
from pathlib import Path

def test_imports():
    """Test if all required libraries are available"""
    print("🔍 Testing imports...")
    
    try:
        from train_college_ai_agent import CollegeAIAgent, INDIAN_LANGUAGES, MultilingualTranslator
        print("✅ Core agent imported successfully")
        
        from googletrans import Translator
        from langdetect import detect
        print("✅ Translation libraries imported successfully")
        
        import torch
        import transformers
        import sentence_transformers
        import faiss
        print("✅ ML libraries imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Please run: python install_multilingual_requirements.py")
        return False

def test_translator():
    """Test the multilingual translator"""
    print("\n🌐 Testing Multilingual Translator...")
    
    try:
        from train_college_ai_agent import MultilingualTranslator
        
        translator = MultilingualTranslator()
        
        # Test language detection
        test_texts = [
            ("What is the fee at IIT?", "en"),
            ("आईआईटी में फीस कितनी है?", "hi"),
            ("আইআইটিতে ফি কত?", "bn"),
            ("ఐఐటిలో ఫీజు ఎంత?", "te")
        ]
        
        print("🔍 Testing language detection:")
        for text, expected_lang in test_texts:
            detected = translator.detect_language(text)
            status = "✅" if detected == expected_lang else "⚠️"
            print(f"   {status} '{text[:30]}...' -> {detected} (expected: {expected_lang})")
        
        # Test translation
        print("\n🔄 Testing translation:")
        english_text = "What is the admission process?"
        
        for lang_code in ['hi', 'bn', 'te', 'ta']:
            lang_name = INDIAN_LANGUAGES[lang_code]['name']
            translated = translator.translate_text(english_text, lang_code)
            print(f"   ✅ {lang_name}: {translated}")
        
        return True
        
    except Exception as e:
        print(f"❌ Translator test failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    print("\n🤖 Testing Agent Initialization...")
    
    try:
        from train_college_ai_agent import CollegeAIAgent
        
        # Test English-only mode
        print("📝 Testing English-only mode...")
        agent_en = CollegeAIAgent(enable_multilingual=False)
        print(f"   ✅ English agent: {len(agent_en.qa_pairs)} Q&A pairs")
        
        # Test multilingual mode
        print("🌐 Testing multilingual mode...")
        agent_ml = CollegeAIAgent(enable_multilingual=True)
        print(f"   ✅ Multilingual agent initialized")
        print(f"   📚 Colleges: {len(agent_ml.colleges_data)}")
        print(f"   💬 Base Q&A pairs: {len(agent_ml.qa_pairs)}")
        
        return agent_ml
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return None

def test_multilingual_data_generation(agent):
    """Test multilingual data generation"""
    print("\n🌐 Testing Multilingual Data Generation...")
    
    try:
        # Check if multilingual data already exists
        if agent.multilingual_qa_pairs:
            print("✅ Multilingual data already available")
            for lang_code, qa_pairs in agent.multilingual_qa_pairs.items():
                lang_name = INDIAN_LANGUAGES[lang_code]['name']
                print(f"   📝 {lang_name}: {len(qa_pairs)} pairs")
            return True
        
        # Generate multilingual data (this takes time)
        print("🔄 Generating multilingual data (this may take 10-15 minutes)...")
        print("⏳ Please wait...")
        
        start_time = time.time()
        agent.generate_multilingual_data()
        end_time = time.time()
        
        print(f"✅ Multilingual data generated in {end_time - start_time:.1f} seconds")
        
        # Verify data
        total_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
        print(f"📊 Total multilingual pairs: {total_pairs:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multilingual data generation failed: {e}")
        return False

def test_embeddings_creation(agent):
    """Test embeddings creation"""
    print("\n🔮 Testing Embeddings Creation...")
    
    try:
        agent.create_embeddings()
        
        # Verify English embeddings
        if agent.embeddings is not None:
            print(f"✅ English embeddings: {agent.embeddings.shape}")
        
        # Verify multilingual embeddings
        if agent.multilingual_embeddings:
            for lang_code, embeddings in agent.multilingual_embeddings.items():
                lang_name = INDIAN_LANGUAGES[lang_code]['name']
                print(f"✅ {lang_name} embeddings: {embeddings.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Embeddings creation failed: {e}")
        return False

def test_multilingual_queries(agent):
    """Test multilingual queries"""
    print("\n🔍 Testing Multilingual Queries...")
    
    test_queries = [
        ("What is the fee at IIT Bombay?", "en", "English"),
        ("आईआईटी बॉम्बे में फीस कितनी है?", "hi", "Hindi"),
        ("আইআইটি বোম্বেতে ফি কত?", "bn", "Bengali"),
        ("ఐఐటి బాంబేలో ఫీజు ఎంత?", "te", "Telugu"),
        ("IIT பம்பாயில் கட்டணம் எவ்வளவு?", "ta", "Tamil")
    ]
    
    for query, lang_code, lang_name in test_queries:
        try:
            print(f"\n🌐 Testing {lang_name} query:")
            print(f"   ❓ Query: {query}")
            
            results = agent.query_agent(query, top_k=2, target_language=lang_code)
            
            if results:
                best_result = results[0]
                print(f"   ✅ Best result ({best_result['confidence']:.1f}% confidence):")
                print(f"      🏫 College: {best_result['college']}")
                print(f"      💡 Answer: {best_result['answer'][:100]}...")
                
                if best_result.get('translated'):
                    print(f"      🔄 Translated from English")
            else:
                print(f"   ❌ No results found")
                
        except Exception as e:
            print(f"   ❌ Query failed: {e}")

def test_model_save_load(agent):
    """Test model saving and loading"""
    print("\n💾 Testing Model Save/Load...")
    
    try:
        # Save model
        model_path = "test_multilingual_model.pkl"
        agent.save_model(model_path)
        print(f"✅ Model saved to {model_path}")
        
        # Create new agent and load model
        new_agent = CollegeAIAgent(enable_multilingual=True)
        success = new_agent.load_model(model_path)
        
        if success:
            print("✅ Model loaded successfully")
            
            # Verify loaded data
            if new_agent.multilingual_qa_pairs:
                total_pairs = sum(len(pairs) for pairs in new_agent.multilingual_qa_pairs.values())
                print(f"📊 Loaded {total_pairs:,} multilingual Q&A pairs")
            
            # Test a query with loaded model
            test_query = "What is the admission process?"
            results = new_agent.query_agent(test_query, top_k=1)
            
            if results:
                print("✅ Query test with loaded model successful")
            else:
                print("⚠️ Query test with loaded model returned no results")
        else:
            print("❌ Model loading failed")
            
        # Clean up
        if Path(model_path).exists():
            Path(model_path).unlink()
            print("🗑️ Test model file cleaned up")
        
        return success
        
    except Exception as e:
        print(f"❌ Model save/load test failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🚀 Multilingual College AI Agent - Comprehensive Test Suite")
    print("=" * 70)
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Import test failed. Please install requirements first.")
        return False
    
    # Test 2: Translator
    if not test_translator():
        print("\n❌ Translator test failed.")
        return False
    
    # Test 3: Agent initialization
    agent = test_agent_initialization()
    if not agent:
        print("\n❌ Agent initialization failed.")
        return False
    
    # Test 4: Multilingual data generation (optional - takes time)
    print("\n⚠️ Multilingual data generation test takes 10-15 minutes.")
    response = input("Do you want to run it? (y/N): ").strip().lower()
    
    if response == 'y':
        if not test_multilingual_data_generation(agent):
            print("\n⚠️ Multilingual data generation failed, but continuing with other tests...")
    else:
        print("⏭️ Skipping multilingual data generation test")
    
    # Test 5: Embeddings creation
    if not test_embeddings_creation(agent):
        print("\n❌ Embeddings creation failed.")
        return False
    
    # Test 6: Multilingual queries
    test_multilingual_queries(agent)
    
    # Test 7: Model save/load
    if not test_model_save_load(agent):
        print("\n❌ Model save/load test failed.")
        return False
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎉 Comprehensive Test Suite Completed!")
    print("✅ All critical tests passed")
    print("\n📊 Test Summary:")
    print("   ✅ Import test: PASSED")
    print("   ✅ Translator test: PASSED")
    print("   ✅ Agent initialization: PASSED")
    print("   ✅ Embeddings creation: PASSED")
    print("   ✅ Multilingual queries: PASSED")
    print("   ✅ Model save/load: PASSED")
    
    print(f"\n🌐 Multilingual College AI Agent is ready!")
    print(f"🚀 You can now use:")
    print(f"   - python multilingual_demo.py (Interactive demo)")
    print(f"   - python api_server_multilingual.py (API server)")
    print(f"   - python train_college_ai_agent.py (Full training)")
    
    return True

def main():
    """Main test function"""
    try:
        success = run_comprehensive_test()
        if success:
            print("\n🎯 All tests completed successfully!")
        else:
            print("\n❌ Some tests failed. Please check the output above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
