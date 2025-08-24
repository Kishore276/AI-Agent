#!/usr/bin/env python3
"""
Load and Run College AI Agent from .h5 Model
Cross-platform deployment script - no retraining needed!
"""

import os
import sys
import time
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        "college_ai_multilingual_complete.h5",
        "college_data"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n📋 Required files for deployment:")
        print("   1. college_ai_multilingual_complete.h5 (trained model)")
        print("   2. college_data/ (college database folder)")
        print("\n💡 Copy these files from the training system")
        return False
    
    return True

def install_requirements():
    """Install required packages"""
    packages = [
        "torch",
        "transformers", 
        "sentence-transformers",
        "scikit-learn",
        "faiss-cpu",
        "h5py",
        "googletrans==3.1.0a0",
        "langdetect",
        "flask"
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {package}")
            else:
                print(f"   ⚠️  {package} - may already be installed")
        except Exception as e:
            print(f"   ❌ {package} - {e}")

def main():
    """Main function to load and run the model"""
    print("🚀 College AI Agent - H5 Model Deployment")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Install packages if needed
    try:
        import torch
        import h5py
        from train_gpu_optimized import load_model_from_h5
        print("✅ All packages available")
    except ImportError:
        print("📦 Installing missing packages...")
        install_requirements()
        print("✅ Packages installed - please restart the script")
        return
    
    # Load model from H5
    print("\n📂 Loading model from H5 file...")
    start_time = time.time()
    
    agent = load_model_from_h5("college_ai_multilingual_complete.h5")
    
    if agent is None:
        print("❌ Failed to load model")
        return
    
    load_time = time.time() - start_time
    print(f"✅ Model loaded in {load_time:.1f} seconds")
    
    # Display model info
    print(f"\n📊 Model Information:")
    print(f"   📚 Colleges: {len(agent.colleges_data)}")
    print(f"   💬 English Q&A pairs: {len(agent.qa_pairs):,}")
    
    if agent.multilingual_qa_pairs:
        total_ml_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
        print(f"   🌐 Multilingual Q&A pairs: {total_ml_pairs:,}")
        print(f"   🗣️  Supported languages: {len(agent.multilingual_qa_pairs)}")
    
    # Test queries
    print(f"\n🧪 Testing Model Performance:")
    test_queries = [
        ("What is the fee at IIT Bombay?", "en", "English"),
        ("आईआईटी बॉम्बे में फीस कितनी है?", "hi", "Hindi"),
        ("Which companies visit for placements?", "en", "English")
    ]
    
    for query, lang_code, lang_name in test_queries:
        try:
            test_start = time.time()
            results = agent.query_agent(query, top_k=2, target_language=lang_code)
            test_time = time.time() - test_start
            
            if results:
                best_result = results[0]
                print(f"✅ {lang_name}: {test_time:.3f}s ({best_result['confidence']:.1f}% confidence)")
                print(f"   🏫 {best_result['college']}")
                print(f"   💡 {best_result['answer'][:100]}...")
            else:
                print(f"⚠️  {lang_name}: {test_time:.3f}s (no results)")
                
        except Exception as e:
            print(f"❌ {lang_name}: Test failed - {e}")
    
    # Start interactive mode
    print(f"\n🎮 Interactive Mode - Ask questions in any language!")
    print("Type 'quit' to exit, 'api' to start API server")
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if query.lower() == 'api':
                print("🌐 Starting API server...")
                try:
                    from api_server_multilingual import app
                    app.run(host='0.0.0.0', port=5000, debug=False)
                except ImportError:
                    print("❌ API server not available - copy api_server_multilingual.py")
                continue
            
            if not query:
                continue
            
            print("🔍 Processing...")
            results = agent.query_agent(query, top_k=2)
            
            if results:
                best_result = results[0]
                print(f"\n🎯 Best Answer ({best_result['confidence']:.1f}% confidence):")
                print(f"🏫 College: {best_result['college']}")
                print(f"📝 Category: {best_result['category']}")
                print(f"💡 Answer: {best_result['answer']}")
                
                if len(results) > 1:
                    print(f"\n📚 Alternative answer:")
                    print(f"🏫 {results[1]['college']}: {results[1]['answer'][:100]}...")
            else:
                print("❌ No relevant answers found")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
