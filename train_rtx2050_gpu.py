#!/usr/bin/env python3
"""
RTX 2050 GPU-Only Training for College AI Agent
Optimized for RTX 2050 4GB VRAM - GPU ONLY, no CPU fallback
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

def check_rtx2050_gpu():
    """Check if RTX 2050 GPU is available and ready"""
    if not torch.cuda.is_available():
        print("❌ CUDA not available - GPU training not possible")
        print("🛑 Stopping as requested - no CPU fallback")
        sys.exit(1)
    
    device = torch.device('cuda')
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    
    print(f"🚀 GPU Detected: {gpu_name}")
    print(f"💾 GPU Memory: {gpu_memory:.1f} GB")
    
    # Check if it's RTX 2050
    if 'RTX 2050' not in gpu_name:
        print(f"⚠️  Expected RTX 2050, found: {gpu_name}")
        response = input("Continue with this GPU? (y/N): ").strip().lower()
        if response != 'y':
            print("🛑 Stopping as requested")
            sys.exit(1)
    
    # RTX 2050 specific optimizations (4GB VRAM)
    if gpu_memory < 3.5:  # Less than 3.5GB available
        print("❌ Insufficient GPU memory for training")
        print("🛑 Stopping as requested - need at least 3.5GB VRAM")
        sys.exit(1)
    
    # Optimize for RTX 2050's 4GB VRAM
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = False
    torch.cuda.set_per_process_memory_fraction(0.80)  # Use 80% of 4GB = ~3.2GB
    
    print("⚡ RTX 2050 optimizations applied")
    print("💾 Memory allocation: 80% of 4GB (~3.2GB)")
    
    return device, gpu_name

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
    """Main RTX 2050 GPU-only training function"""
    print("🚀 RTX 2050 GPU-Only College AI Agent Training")
    print("=" * 60)
    
    # Check RTX 2050 GPU availability (will exit if not available)
    device, gpu_name = check_rtx2050_gpu()
    
    # Count data
    num_colleges, num_files = count_colleges()
    print(f"📚 Dataset: {num_colleges} colleges, {num_files} data files")
    
    if num_colleges == 0:
        print("❌ No college data found. Please ensure college_data directory exists.")
        sys.exit(1)
    
    # Import and initialize agent
    try:
        from train_college_ai_agent import CollegeAIAgent
        print("✅ Multilingual agent imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Please run: python install_multilingual_requirements.py")
        sys.exit(1)
    
    # Initialize agent with multilingual support
    print(f"\n🤖 Initializing AI Agent on {gpu_name}...")
    start_time = time.time()
    
    try:
        # Initialize with multilingual enabled
        agent = CollegeAIAgent(enable_multilingual=True)
        init_time = time.time() - start_time
        
        print(f"✅ Agent initialized in {init_time:.1f} seconds")
        print(f"📊 Loaded {len(agent.colleges_data)} colleges")
        print(f"💬 Generated {len(agent.qa_pairs)} English Q&A pairs")
        
        # Check GPU memory usage after initialization
        if torch.cuda.is_available():
            memory_allocated = torch.cuda.memory_allocated() / 1024**3
            memory_reserved = torch.cuda.memory_reserved() / 1024**3
            print(f"💾 GPU Memory - Allocated: {memory_allocated:.2f}GB, Reserved: {memory_reserved:.2f}GB")
        
        # Check if translator is available
        if agent.translator:
            languages = agent.get_supported_languages()
            print(f"🌐 Translation support: {len(languages)} languages available")
        else:
            print("⚠️  Translation not available - English only mode")
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        sys.exit(1)
    
    # Create embeddings on RTX 2050
    print(f"\n🔮 Creating Embeddings on RTX 2050...")
    embed_start = time.time()
    
    try:
        # Clear GPU cache before embeddings
        torch.cuda.empty_cache()
        gc.collect()
        
        # Monitor GPU memory before embeddings
        memory_before = torch.cuda.memory_allocated() / 1024**3
        print(f"💾 GPU Memory before embeddings: {memory_before:.2f}GB")
        
        # Create embeddings with GPU acceleration
        agent.create_embeddings()
        embed_time = time.time() - embed_start
        
        # Monitor GPU memory after embeddings
        memory_after = torch.cuda.memory_allocated() / 1024**3
        print(f"💾 GPU Memory after embeddings: {memory_after:.2f}GB")
        
        print(f"✅ Embeddings created in {embed_time:.1f} seconds")
        print(f"📊 English embeddings: {agent.embeddings.shape}")
        
    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            print(f"❌ GPU Out of Memory: {e}")
            print("🛑 RTX 2050 4GB VRAM insufficient for this dataset size")
            print("💡 Try reducing batch size or dataset size")
            sys.exit(1)
        else:
            print(f"❌ GPU Error: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Embedding creation failed: {e}")
        sys.exit(1)
    
    # Train response model
    print(f"\n🎓 Training Response Model on GPU...")
    try:
        agent.train_response_model()
        print(f"✅ Response model training completed")
    except Exception as e:
        print(f"⚠️  Response model training failed: {e}")
        print("📝 Continuing without response model")
    
    # Save the model
    print(f"\n💾 Saving RTX 2050 Trained Model...")
    save_start = time.time()
    
    try:
        model_filename = f"college_ai_rtx2050_trained.pkl"
        agent.save_model(model_filename)
        save_time = time.time() - save_start
        
        # Get file size
        model_size = Path(model_filename).stat().st_size / (1024**2)  # MB
        
        print(f"✅ Model saved as {model_filename}")
        print(f"📁 Model size: {model_size:.1f} MB")
        print(f"⏱️  Save time: {save_time:.1f} seconds")
        
    except Exception as e:
        print(f"❌ Model saving failed: {e}")
        sys.exit(1)
    
    # Test GPU performance
    print(f"\n🧪 Testing GPU Performance...")
    test_queries = [
        ("What is the fee at IIT Bombay?", "en", "English"),
        ("आईआईटी बॉम्बे में फीस कितनी है?", "hi", "Hindi"),
        ("Which companies visit for placements?", "en", "English")
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
                successful_tests += 1
            else:
                print(f"⚠️  {lang_name}: {test_time:.3f}s (no results)")
                
        except Exception as e:
            print(f"❌ {lang_name}: Test failed - {e}")
    
    avg_response_time = total_test_time / len(test_queries) if test_queries else 0
    
    # Final GPU memory check
    final_memory = torch.cuda.memory_allocated() / 1024**3
    max_memory = torch.cuda.max_memory_allocated() / 1024**3
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n" + "=" * 60)
    print(f"🎉 RTX 2050 GPU Training Completed Successfully!")
    print(f"⏱️  Total time: {total_time/60:.1f} minutes")
    print(f"🚀 GPU: {gpu_name}")
    
    print(f"\n📊 Training Statistics:")
    print(f"   📚 Colleges: {len(agent.colleges_data)}")
    print(f"   💬 Q&A pairs: {len(agent.qa_pairs):,}")
    print(f"   🔮 Embeddings: {agent.embeddings.shape}")
    print(f"   ⚡ Avg response time: {avg_response_time:.3f}s")
    print(f"   🎯 Test success rate: {successful_tests}/{len(test_queries)}")
    
    print(f"\n💾 GPU Memory Usage:")
    print(f"   📊 Final allocated: {final_memory:.2f}GB")
    print(f"   📈 Peak usage: {max_memory:.2f}GB")
    print(f"   💡 RTX 2050 utilization: {max_memory/4*100:.1f}% of 4GB")
    
    print(f"\n🚀 Model Ready:")
    print(f"   📁 Model file: {model_filename}")
    print(f"   🌐 API server: python api_server_multilingual.py")
    print(f"   🎮 Demo: python multilingual_demo.py")
    
    # GPU cleanup
    torch.cuda.empty_cache()
    gc.collect()
    print(f"\n🧹 RTX 2050 GPU memory cleaned up")
    print(f"✨ Training completed successfully on RTX 2050!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⏹️  Training interrupted by user")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        sys.exit(1)
