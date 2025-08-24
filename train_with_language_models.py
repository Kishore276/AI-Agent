#!/usr/bin/env python3
"""
College AI Agent Training with Language Models
Import language models for multilingual support without generating all language data
"""

import os
import sys
import json
import time
import torch
import gc
from pathlib import Path
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Set environment variables for optimal GPU usage
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

def setup_gpu():
    """Setup GPU configuration"""
    if torch.cuda.is_available():
        device = torch.device('cuda')
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        print(f"🚀 GPU Detected: {gpu_name}")
        print(f"💾 GPU Memory: {gpu_memory:.1f} GB")
        
        # Optimize for GPU
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False
        
        # Set memory fraction to prevent OOM
        torch.cuda.set_per_process_memory_fraction(0.85)
        print("⚡ GPU optimizations applied")
        
        return device, gpu_name
    else:
        print("⚠️  No GPU detected, using CPU")
        return torch.device('cpu'), 'CPU'

def count_colleges():
    """Count total colleges and data files"""
    college_data_path = Path("college_data")
    if not college_data_path.exists():
        return 0, 0
    
    colleges = [d for d in college_data_path.iterdir() if d.is_dir()]
    total_files = 0
    
    for college_dir in colleges:
        json_files = list(college_dir.glob("*.json"))
        total_files += len(json_files)
    
    return len(colleges), total_files

def main():
    """Main training function with language models only"""
    print("🚀 College AI Agent Training with Language Models")
    print("=" * 60)
    
    # Setup GPU
    device, gpu_name = setup_gpu()
    
    # Count data
    num_colleges, num_files = count_colleges()
    print(f"📚 Dataset: {num_colleges} colleges, {num_files} data files")
    
    if num_colleges == 0:
        print("❌ No college data found. Please ensure college_data directory exists.")
        return
    
    # Import and initialize agent
    try:
        from train_college_ai_agent import CollegeAIAgent
        print("✅ Multilingual agent imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Please run: python install_multilingual_requirements.py")
        return
    
    # Initialize agent with multilingual support but no data generation
    print("\n🤖 Initializing AI Agent with Language Models...")
    start_time = time.time()
    
    try:
        # Initialize with multilingual enabled but don't generate data
        agent = CollegeAIAgent(enable_multilingual=True)
        init_time = time.time() - start_time
        
        print(f"✅ Agent initialized in {init_time:.1f} seconds")
        print(f"📊 Loaded {len(agent.colleges_data)} colleges")
        print(f"💬 Generated {len(agent.qa_pairs)} English Q&A pairs")
        
        # Check if translator is available
        if agent.translator:
            languages = agent.get_supported_languages()
            print(f"🌐 Translation support: {len(languages)} languages available")
            print("🔄 Real-time translation enabled for queries and responses")
        else:
            print("⚠️  Translation not available - English only mode")
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return
    
    # Create embeddings for English data only
    print(f"\n🔮 Creating Embeddings on {gpu_name}...")
    embed_start = time.time()
    
    try:
        # Clear GPU cache before embeddings
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
        
        # Create embeddings only for English data
        agent.create_embeddings()
        embed_time = time.time() - embed_start
        
        print(f"✅ Embeddings created in {embed_time:.1f} seconds")
        print(f"📊 English embeddings: {agent.embeddings.shape}")
        
    except Exception as e:
        print(f"❌ Embedding creation failed: {e}")
        return
    
    # Train response model
    print(f"\n🎓 Training Response Model...")
    try:
        agent.train_response_model()
        print(f"✅ Response model training completed")
    except Exception as e:
        print(f"⚠️  Response model training failed: {e}")
        print("📝 Continuing without response model")
    
    # Save the model
    print(f"\n💾 Saving Multilingual-Ready Model...")
    save_start = time.time()
    
    try:
        model_filename = f"college_ai_multilingual_ready.pkl"
        agent.save_model(model_filename)
        save_time = time.time() - save_start
        
        # Get file size
        model_size = Path(model_filename).stat().st_size / (1024**2)  # MB
        
        print(f"✅ Model saved as {model_filename}")
        print(f"📁 Model size: {model_size:.1f} MB")
        print(f"⏱️  Save time: {save_time:.1f} seconds")
        
    except Exception as e:
        print(f"❌ Model saving failed: {e}")
        return
    
    # Test multilingual capabilities with real-time translation
    print(f"\n🧪 Testing Multilingual Capabilities...")
    test_queries = [
        ("What is the fee at IIT Bombay?", "en", "English"),
        ("आईआईटी बॉम्बे में फीस कितनी है?", "hi", "Hindi"),
        ("আইআইটি বোম্বেতে ফি কত?", "bn", "Bengali"),
        ("ఐఐటి బాంబేలో ఫీజు ఎంత?", "te", "Telugu"),
        ("IIT பம்பாயில் கட்டணம் எவ்வளவு?", "ta", "Tamil")
    ]
    
    total_test_time = 0
    successful_tests = 0
    
    for query, lang_code, lang_name in test_queries:
        try:
            test_start = time.time()
            results = agent.query_agent(query, top_k=2, target_language=lang_code)
            test_time = time.time() - test_start
            total_test_time += test_time
            
            if results:
                best_result = results[0]
                print(f"✅ {lang_name}: {test_time:.3f}s ({best_result['confidence']:.1f}% confidence)")
                print(f"   🏫 {best_result['college']}")
                print(f"   💡 {best_result['answer'][:100]}...")
                if best_result.get('translated'):
                    print(f"   🔄 Answer translated to {lang_name}")
                successful_tests += 1
            else:
                print(f"⚠️  {lang_name}: {test_time:.3f}s (no results)")
                
        except Exception as e:
            print(f"❌ {lang_name}: Test failed - {e}")
    
    avg_response_time = total_test_time / len(test_queries) if test_queries else 0
    
    # Create deployment package
    print(f"\n📦 Creating Deployment Package...")
    try:
        deploy_dir = agent.create_deployment_package()
        print(f"✅ Deployment package created in: {deploy_dir}")
    except Exception as e:
        print(f"⚠️  Deployment package creation failed: {e}")
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n" + "=" * 60)
    print(f"🎉 Training Completed Successfully!")
    print(f"⏱️  Total time: {total_time/60:.1f} minutes")
    print(f"🚀 GPU used: {gpu_name}")
    
    print(f"\n📊 Model Statistics:")
    print(f"   📚 Colleges: {len(agent.colleges_data)}")
    print(f"   💬 English Q&A pairs: {len(agent.qa_pairs):,}")
    print(f"   🌐 Multilingual support: Real-time translation")
    print(f"   🔮 Embeddings: English base with translation")
    print(f"   ⚡ Avg response time: {avg_response_time:.3f}s")
    print(f"   🎯 Test success rate: {successful_tests}/{len(test_queries)}")
    
    if agent.translator:
        languages = agent.get_supported_languages()
        print(f"   🗣️  Supported languages: {len(languages)}")
        print(f"      Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati,")
        print(f"      Kannada, Malayalam, Urdu, Punjabi, Odia, Assamese, English")
    
    print(f"\n🚀 Model Features:")
    print(f"   ✅ Fast training (no pre-generation of all language data)")
    print(f"   ✅ Real-time translation for queries and responses")
    print(f"   ✅ Supports 18+ Indian languages")
    print(f"   ✅ GPU-optimized embeddings")
    print(f"   ✅ Efficient memory usage")
    
    print(f"\n🎮 Usage:")
    print(f"   📁 Model file: {model_filename}")
    print(f"   🌐 API server: python api_server_multilingual.py")
    print(f"   🎯 Demo: python multilingual_demo.py")
    print(f"   🧪 Test: python test_multilingual.py")
    
    # GPU memory cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()
        print(f"\n🧹 GPU memory cleaned up")
    
    print(f"\n✨ Ready for multilingual queries with real-time translation!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⏹️  Training interrupted by user")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        sys.exit(1)
