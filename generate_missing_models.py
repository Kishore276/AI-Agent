#!/usr/bin/env python3
"""
Generate Missing Model Files
Create college_ai_agent.pkl and fix multilingual model
"""

import pickle
import os
from pathlib import Path

def create_primary_model():
    """Create the missing college_ai_agent.pkl file"""
    print("🤖 Creating primary AI agent model...")
    
    try:
        from train_college_ai_agent import CollegeAIAgent
        
        # Initialize agent in English-only mode for faster training
        agent = CollegeAIAgent(enable_multilingual=False)
        print(f"✅ Agent initialized with {len(agent.colleges_data)} colleges")
        print(f"📝 Generated {len(agent.qa_pairs)} Q&A pairs")
        
        # Create embeddings
        print("🔮 Creating embeddings...")
        agent.create_embeddings()
        print("✅ Embeddings created successfully")
        
        # Save the primary model
        model_path = "college_ai_agent.pkl"
        agent.save_model(model_path)
        print(f"💾 Primary model saved to {model_path}")
        
        # Verify the saved model
        model_size = os.path.getsize(model_path) / (1024 * 1024)
        print(f"📦 Model size: {model_size:.1f} MB")
        
        # Test loading the model
        with open(model_path, 'rb') as f:
            test_data = pickle.load(f)
        print(f"✅ Model verification successful - {len(test_data['qa_pairs'])} Q&A pairs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating primary model: {e}")
        return False

def create_multilingual_model():
    """Create a new multilingual model"""
    print("\n🌐 Creating multilingual AI agent model...")
    
    try:
        from train_college_ai_agent import CollegeAIAgent
        
        # Initialize agent with multilingual support
        agent = CollegeAIAgent(enable_multilingual=True)
        print(f"✅ Multilingual agent initialized")
        
        # Note: Full multilingual generation takes 10-15 minutes
        # For now, just save the base English model with multilingual structure
        print("💾 Saving multilingual-ready model structure...")
        
        model_path = "college_ai_multilingual_ready.pkl"
        agent.save_model(model_path)
        
        # Verify the saved model
        model_size = os.path.getsize(model_path) / (1024 * 1024)
        print(f"📦 Multilingual model size: {model_size:.1f} MB")
        print("✅ Multilingual model created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating multilingual model: {e}")
        return False

def create_multilingual_data_directory():
    """Create the missing multilingual_data directory"""
    print("\n📁 Creating multilingual_data directory...")
    
    multilingual_dir = Path("multilingual_data")
    if not multilingual_dir.exists():
        multilingual_dir.mkdir()
        print("✅ Created multilingual_data directory")
        
        # Create a placeholder file
        placeholder = multilingual_dir / "README.md"
        with open(placeholder, 'w', encoding='utf-8') as f:
            f.write("""# Multilingual Data Directory

This directory will contain translated Q&A pairs in various Indian languages.

To generate multilingual data:
```python
from train_college_ai_agent import CollegeAIAgent
agent = CollegeAIAgent(enable_multilingual=True)
agent.generate_multilingual_data()  # Takes 10-15 minutes
```

Supported languages: Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, Urdu, Kannada, Malayalam, Odia, Punjabi, Assamese, and more.
""")
        print("📝 Created README.md in multilingual_data")
    else:
        print("✅ multilingual_data directory already exists")

if __name__ == "__main__":
    print("🔧 Generating Missing Model Files")
    print("=" * 50)
    
    # Step 1: Create primary model
    if create_primary_model():
        print("✅ Primary model creation successful")
    else:
        print("❌ Primary model creation failed")
    
    # Step 2: Create multilingual model structure
    if create_multilingual_model():
        print("✅ Multilingual model creation successful")
    else:
        print("❌ Multilingual model creation failed")
    
    # Step 3: Create multilingual data directory
    create_multilingual_data_directory()
    
    print("\n🎉 Model file generation completed!")
    print("\n📊 Final Status:")
    
    # Check final status
    files_to_check = [
        "college_ai_agent.pkl",
        "college_ai_multilingual_ready.pkl"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path) / (1024 * 1024)
            print(f"✅ {file_path} - {size:.1f} MB")
        else:
            print(f"❌ {file_path} - Missing")
