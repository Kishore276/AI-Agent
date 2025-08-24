import pickle
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class CollegeAIQuery:
    def __init__(self, model_path='college_ai_model.pkl'):
        print("Loading College AI Agent...")

        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)

        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_pairs = model_data['qa_pairs']
        self.embeddings = model_data['embeddings']

        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

        print(f"Loaded {len(self.qa_pairs)} Q&A pairs from {len(set(qa['college'] for qa in self.qa_pairs))} colleges")

    def query(self, question, top_k=5):
        """Query the AI agent"""
        question_embedding = self.sentence_model.encode([question])
        faiss.normalize_L2(question_embedding)

        scores, indices = self.index.search(question_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.qa_pairs):
                qa = self.qa_pairs[idx]
                results.append({
                    'college': qa['college'],
                    'category': qa['category'],
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'confidence': float(score) * 100
                })

        return results

def main():
    agent = CollegeAIQuery()

    print("\nCollege AI Agent Ready!")
    print("Ask questions about engineering colleges (type 'quit' to exit)\n")

    while True:
        try:
            question = input("❓ Your question: ").strip()

            if question.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            if not question:
                continue

            results = agent.query(question, top_k=3)

            if results:
                best = results[0]
                print(f"\nBest Answer ({best['confidence']:.1f}% confidence):")
                print(f"College: {best['college']}")
                print(f"Answer: {best['answer']}\n")

                if len(results) > 1:
                    print("Other relevant answers:")
                    for i, result in enumerate(results[1:], 2):
                        print(f"   {i}. {result['college']}: {result['answer'][:100]}...")
            else:
                print("No relevant answers found")

            print("-" * 60)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()