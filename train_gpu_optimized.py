#!/usr/bin/env python3
"""
GPU-Optimized Multilingual College AI Agent Training
Optimized for T4 GPU with efficient memory management and batch processing
"""

import os
import sys
import json
import time
import torch
import gc
import h5py
import numpy as np
from pathlib import Path
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Set environment variables for optimal GPU usage
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

def setup_gpu():
    """Setup GPU configuration for T4 optimization"""
    if torch.cuda.is_available():
        device = torch.device('cuda')
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        print(f"🚀 GPU Detected: {gpu_name}")
        print(f"💾 GPU Memory: {gpu_memory:.1f} GB")
        
        # Optimize for T4 GPU
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False
        
        # Set memory fraction to prevent OOM
        if 'T4' in gpu_name:
            torch.cuda.set_per_process_memory_fraction(0.85)  # Use 85% of T4's 16GB
            print("⚡ T4 GPU optimizations applied")
        
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

def save_model_as_h5(agent, model_path: str = "college_ai_multilingual_complete.h5"):
    """Save the complete multilingual model as .h5 file for cross-platform deployment"""
    print(f"\n💾 Saving Complete Model as .h5 format...")

    try:
        with h5py.File(model_path, 'w') as h5f:
            # Save basic model info
            h5f.attrs['model_version'] = '1.0'
            h5f.attrs['creation_date'] = str(time.time())
            h5f.attrs['total_colleges'] = len(agent.colleges_data)
            h5f.attrs['total_qa_pairs'] = len(agent.qa_pairs)
            h5f.attrs['multilingual_enabled'] = agent.enable_multilingual

            # Save colleges data
            colleges_group = h5f.create_group('colleges_data')
            colleges_json = json.dumps(agent.colleges_data, ensure_ascii=False)
            colleges_group.create_dataset('data', data=colleges_json.encode('utf-8'))

            # Save English Q&A pairs
            qa_group = h5f.create_group('qa_pairs')
            qa_json = json.dumps(agent.qa_pairs, ensure_ascii=False)
            qa_group.create_dataset('english', data=qa_json.encode('utf-8'))

            # Save English embeddings
            if agent.embeddings is not None:
                embeddings_group = h5f.create_group('embeddings')
                embeddings_group.create_dataset('english', data=agent.embeddings)
                embeddings_group.attrs['shape'] = agent.embeddings.shape
                embeddings_group.attrs['dtype'] = str(agent.embeddings.dtype)

            # Save multilingual data if available
            if agent.multilingual_qa_pairs:
                multilingual_group = h5f.create_group('multilingual_qa_pairs')
                for lang_code, qa_pairs in agent.multilingual_qa_pairs.items():
                    lang_json = json.dumps(qa_pairs, ensure_ascii=False)
                    multilingual_group.create_dataset(lang_code, data=lang_json.encode('utf-8'))

                h5f.attrs['total_multilingual_pairs'] = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
                h5f.attrs['supported_languages'] = len(agent.multilingual_qa_pairs)

            # Save multilingual embeddings if available
            if agent.multilingual_embeddings:
                ml_embeddings_group = h5f.create_group('multilingual_embeddings')
                for lang_code, embeddings in agent.multilingual_embeddings.items():
                    ml_embeddings_group.create_dataset(lang_code, data=embeddings)

            # Save supported languages list
            from train_college_ai_agent import INDIAN_LANGUAGES
            languages_json = json.dumps(INDIAN_LANGUAGES, ensure_ascii=False)
            h5f.create_dataset('supported_languages', data=languages_json.encode('utf-8'))

        # Get file size
        model_size = Path(model_path).stat().st_size / (1024**2)  # MB

        print(f"✅ Complete model saved as {model_path}")
        print(f"📁 Model size: {model_size:.1f} MB")
        print(f"🌐 Cross-platform deployment ready!")

        return model_path

    except Exception as e:
        print(f"❌ Error saving .h5 model: {e}")
        return None

def load_model_from_h5(model_path: str = "college_ai_multilingual_complete.h5"):
    """Load the complete multilingual model from .h5 file"""
    print(f"📂 Loading model from {model_path}...")

    try:
        from train_college_ai_agent import CollegeAIAgent

        with h5py.File(model_path, 'r') as h5f:
            # Load basic info
            model_version = h5f.attrs.get('model_version', '1.0')
            total_colleges = h5f.attrs.get('total_colleges', 0)
            total_qa_pairs = h5f.attrs.get('total_qa_pairs', 0)
            multilingual_enabled = h5f.attrs.get('multilingual_enabled', False)

            print(f"📊 Model version: {model_version}")
            print(f"📚 Colleges: {total_colleges}")
            print(f"💬 Q&A pairs: {total_qa_pairs}")
            print(f"🌐 Multilingual: {multilingual_enabled}")

            # Initialize agent
            agent = CollegeAIAgent(enable_multilingual=multilingual_enabled)

            # Load colleges data
            colleges_json = h5f['colleges_data']['data'][()].decode('utf-8')
            agent.colleges_data = json.loads(colleges_json)

            # Load English Q&A pairs
            qa_json = h5f['qa_pairs']['english'][()].decode('utf-8')
            agent.qa_pairs = json.loads(qa_json)

            # Load English embeddings
            if 'embeddings' in h5f:
                agent.embeddings = h5f['embeddings']['english'][:]
                print(f"✅ Loaded English embeddings: {agent.embeddings.shape}")

            # Load multilingual data if available
            if 'multilingual_qa_pairs' in h5f:
                agent.multilingual_qa_pairs = {}
                for lang_code in h5f['multilingual_qa_pairs'].keys():
                    lang_json = h5f['multilingual_qa_pairs'][lang_code][()].decode('utf-8')
                    agent.multilingual_qa_pairs[lang_code] = json.loads(lang_json)

                total_ml_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
                print(f"✅ Loaded multilingual Q&A pairs: {total_ml_pairs:,}")

            # Load multilingual embeddings if available
            if 'multilingual_embeddings' in h5f:
                agent.multilingual_embeddings = {}
                for lang_code in h5f['multilingual_embeddings'].keys():
                    agent.multilingual_embeddings[lang_code] = h5f['multilingual_embeddings'][lang_code][:]
                print(f"✅ Loaded multilingual embeddings for {len(agent.multilingual_embeddings)} languages")

            # Recreate FAISS indices
            if agent.embeddings is not None:
                import faiss
                dimension = agent.embeddings.shape[1]
                agent.index = faiss.IndexFlatIP(dimension)
                agent.index.add(agent.embeddings)

                # Recreate multilingual indices
                if agent.multilingual_embeddings:
                    agent.multilingual_indices = {}
                    for lang_code, embeddings in agent.multilingual_embeddings.items():
                        lang_index = faiss.IndexFlatIP(dimension)
                        lang_index.add(embeddings)
                        agent.multilingual_indices[lang_code] = lang_index

            print(f"✅ Model loaded successfully from {model_path}")
            return agent

    except Exception as e:
        print(f"❌ Error loading .h5 model: {e}")
        return None

def main():
    """Main GPU-optimized training function"""
    print("🚀 GPU-Optimized Multilingual College AI Agent Training")
    print("=" * 70)
    
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
    
    # Initialize agent with GPU optimization
    print("\n🤖 Initializing Multilingual AI Agent...")
    start_time = time.time()
    
    try:
        agent = CollegeAIAgent(enable_multilingual=True)
        init_time = time.time() - start_time
        print(f"✅ Agent initialized in {init_time:.1f} seconds")
        print(f"📊 Loaded {len(agent.colleges_data)} colleges")
        print(f"💬 Generated {len(agent.qa_pairs)} base Q&A pairs")
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return
    
    # Check if we should generate multilingual data
    if not agent.multilingual_qa_pairs:
        print(f"\n🌐 Generating Multilingual Data...")
        print(f"⏳ This will create Q&A pairs in 18+ Indian languages")
        print(f"🕐 Estimated time: 15-20 minutes for {len(agent.qa_pairs)} pairs")
        print(f"💾 Memory usage will be optimized for T4 GPU")

        # Auto-proceed for batch training
        print("🚀 Auto-proceeding with multilingual generation for complete training...")

        try:
            ml_start = time.time()

            # Generate multilingual data with memory optimization
            print("🔄 Generating multilingual data in batches...")
            agent.generate_multilingual_data()

            # Clear memory after generation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()

            ml_time = time.time() - ml_start

            total_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
            print(f"✅ Multilingual data generated in {ml_time/60:.1f} minutes")
            print(f"🌐 Total pairs: {total_pairs:,} across {len(agent.multilingual_qa_pairs)} languages")

        except Exception as e:
            print(f"❌ Multilingual generation failed: {e}")
            print("📝 Continuing with English-only model")
    else:
        total_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
        print(f"✅ Multilingual data already available: {total_pairs:,} pairs")
    
    # Create embeddings with GPU optimization
    print(f"\n🔮 Creating Embeddings on {gpu_name}...")
    embed_start = time.time()
    
    try:
        # Clear GPU cache before embeddings
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
        
        agent.create_embeddings()
        embed_time = time.time() - embed_start
        
        print(f"✅ Embeddings created in {embed_time:.1f} seconds")
        
        # Display embedding statistics
        if agent.embeddings is not None:
            print(f"📊 English embeddings: {agent.embeddings.shape}")
        
        if agent.multilingual_embeddings:
            for lang_code, embeddings in agent.multilingual_embeddings.items():
                from train_college_ai_agent import INDIAN_LANGUAGES
                lang_name = INDIAN_LANGUAGES[lang_code]['name']
                print(f"🌐 {lang_name} embeddings: {embeddings.shape}")
        
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
    
    # Save the complete model in both formats
    print(f"\n💾 Saving Complete Multilingual Model...")
    save_start = time.time()

    try:
        # Save as .pkl (original format)
        pkl_filename = f"multilingual_college_ai_gpu_trained.pkl"
        agent.save_model(pkl_filename)
        pkl_size = Path(pkl_filename).stat().st_size / (1024**2)  # MB

        # Save as .h5 (cross-platform format)
        h5_filename = save_model_as_h5(agent, "college_ai_multilingual_complete.h5")
        h5_size = Path(h5_filename).stat().st_size / (1024**2) if h5_filename else 0

        save_time = time.time() - save_start

        print(f"✅ Models saved successfully:")
        print(f"   📁 PKL format: {pkl_filename} ({pkl_size:.1f} MB)")
        print(f"   📁 H5 format: {h5_filename} ({h5_size:.1f} MB)")
        print(f"⏱️  Total save time: {save_time:.1f} seconds")

    except Exception as e:
        print(f"❌ Model saving failed: {e}")
        return
    
    # Create deployment package
    print(f"\n📦 Creating Deployment Package...")
    try:
        deploy_dir = agent.create_deployment_package()
        print(f"✅ Deployment package created in: {deploy_dir}")
    except Exception as e:
        print(f"⚠️  Deployment package creation failed: {e}")
    
    # Performance testing
    print(f"\n🧪 Performance Testing...")
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
            results = agent.query_agent(query, top_k=3, target_language=lang_code)
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
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n" + "=" * 70)
    print(f"🎉 GPU-Optimized Training Completed!")
    print(f"⏱️  Total training time: {total_time/60:.1f} minutes")
    print(f"🚀 GPU used: {gpu_name}")
    print(f"📊 Training Statistics:")
    print(f"   📚 Colleges processed: {len(agent.colleges_data)}")
    
    if agent.multilingual_qa_pairs:
        total_pairs = sum(len(pairs) for pairs in agent.multilingual_qa_pairs.values())
        languages = len(agent.multilingual_qa_pairs)
        print(f"   💬 Total Q&A pairs: {total_pairs:,}")
        print(f"   🌐 Languages supported: {languages}")
    else:
        print(f"   💬 English Q&A pairs: {len(agent.qa_pairs):,}")
        print(f"   🌐 Languages supported: 1 (English only)")
    
    print(f"   🔮 Embeddings created: ✅")
    print(f"   💾 Model saved: ✅")
    print(f"   ⚡ Avg response time: {avg_response_time:.3f}s")
    print(f"   🎯 Test success rate: {successful_tests}/{len(test_queries)}")
    
    print(f"\n🚀 Model Ready for Deployment!")
    print(f"📁 PKL Model: {pkl_filename} (for this system)")
    print(f"📁 H5 Model: college_ai_multilingual_complete.h5 (cross-platform)")
    print(f"🌐 API server: python api_server_multilingual.py")
    print(f"🎮 Demo: python multilingual_demo.py")
    print(f"\n🔄 For deployment on another system:")
    print(f"   1. Copy: college_ai_multilingual_complete.h5")
    print(f"   2. Copy: college_data/ folder")
    print(f"   3. Run: python load_and_run_h5.py")
    print(f"   ✅ No retraining needed!")
    
    # GPU memory cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()
        print(f"🧹 GPU memory cleaned up")

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
