"""
Simple Test of the Trained College AI Agent
"""

import pickle
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def test_ai_agent():
    print("Loading Trained College AI Agent...")
    
    # Load the trained model
    with open('college_ai_agent.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    qa_pairs = model_data['qa_pairs']
    embeddings = model_data['embeddings']
    colleges_data = model_data['colleges_data']
    
    # Initialize sentence transformer
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    print(f"Loaded {len(qa_pairs)} Q&A pairs from {len(colleges_data)} colleges")
    print(f"Embedding dimension: {dimension}")
    
    def query(question, top_k=3):
        """Query the AI agent"""
        question_embedding = sentence_model.encode([question])
        faiss.normalize_L2(question_embedding)
        
        scores, indices = index.search(question_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(qa_pairs):
                qa = qa_pairs[idx]
                results.append({
                    'college': qa['college'],
                    'category': qa['category'],
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'confidence': float(score) * 100
                })
        
        return results
    
    # Test queries
    test_queries = [
        "What is the fee at IIT Bombay?",
        "Which companies visit NIT Trichy for placements?",
        "What is the average package at private colleges?",
        "How to apply for admission in 2025?",
        "What are the facilities at IIIT Hyderabad?"
    ]
    
    print("\nTesting AI Agent:")
    print("=" * 50)
    
    for i, test_query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {test_query}")
        print("-" * 40)
        
        results = query(test_query)
        
        if results:
            best = results[0]
            print(f"Best Answer ({best['confidence']:.1f}% confidence):")
            print(f"College: {best['college']}")
            print(f"Answer: {best['answer'][:200]}...")
            
            if len(results) > 1:
                print(f"\nOther relevant answers:")
                for j, result in enumerate(results[1:], 2):
                    print(f"  {j}. {result['college']} ({result['confidence']:.1f}%)")
        else:
            print("No relevant answers found")
    
    print(f"\nTraining and testing completed successfully!")
    print(f"Model Statistics:")
    print(f"  - Total Colleges: {len(colleges_data)}")
    print(f"  - Total Q&A Pairs: {len(qa_pairs)}")
    print(f"  - Embedding Dimension: {dimension}")
    print(f"  - Model File: college_ai_agent.pkl")
    print(f"  - Deployment Package: college_ai_deployment/")
    
    return True

if __name__ == "__main__":
    try:
        test_ai_agent()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the model file 'college_ai_agent.pkl' exists")
