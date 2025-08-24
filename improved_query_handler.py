#!/usr/bin/env python3
"""
Intelligent Query Handler
Improves query processing to handle general vs specific college questions appropriately
"""

import re
import pickle
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Optional

class ImprovedCollegeAI:
    """Enhanced College AI with intelligent query classification"""
    
    def __init__(self, model_path="college_ai_agent.pkl"):
        print("🚀 Loading Improved College AI Agent...")
        
        # Load the trained model
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.qa_pairs = model_data['qa_pairs']
        self.embeddings = model_data['embeddings']
        self.colleges_data = model_data['colleges_data']
        
        # Initialize sentence transformer
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create FAISS index
        if self.embeddings is not None:
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings)
        
        # Define general vs specific query patterns
        self.general_patterns = [
            r"how to apply for admission",
            r"what is the admission process",
            r"when do applications start",
            r"admission requirements",
            r"what are the fees",
            r"average package",
            r"placement statistics",
            r"best colleges for",
            r"top colleges",
            r"which college is better",
            r"compare colleges",
            r"general information",
            r"overview of",
        ]
        
        self.college_keywords = self.extract_college_keywords()
        
        print(f"✅ Loaded {len(self.qa_pairs)} Q&A pairs from {len(self.colleges_data)} colleges")
    
    def extract_college_keywords(self) -> List[str]:
        """Extract college names and common abbreviations"""
        keywords = set()
        
        for college_name in self.colleges_data.keys():
            # Add full name
            keywords.add(college_name.lower())
            
            # Add common abbreviations
            words = college_name.split()
            if "IIT" in college_name:
                keywords.add("iit")
                # Add city name for IITs
                for word in words:
                    if word not in ["IIT", "Indian", "Institute", "of", "Technology"]:
                        keywords.add(word.lower())
            
            elif "NIT" in college_name:
                keywords.add("nit")
                for word in words:
                    if word not in ["NIT", "National", "Institute", "of", "Technology"]:
                        keywords.add(word.lower())
            
            elif "IIIT" in college_name:
                keywords.add("iiit")
                for word in words:
                    if word not in ["IIIT", "Indian", "Institute", "of", "Information", "Technology"]:
                        keywords.add(word.lower())
            
            # Add significant words from college name
            for word in words:
                if len(word) > 3 and word not in ["College", "Engineering", "Technology", "Institute", "University"]:
                    keywords.add(word.lower())
        
        return list(keywords)
    
    def classify_query(self, question: str) -> Dict[str, any]:
        """Classify if query is general or college-specific"""
        question_lower = question.lower()
        
        # Check for college-specific keywords
        mentioned_colleges = []
        for keyword in self.college_keywords:
            if keyword in question_lower:
                # Find matching college names
                for college_name in self.colleges_data.keys():
                    if keyword in college_name.lower():
                        mentioned_colleges.append(college_name)
        
        # Remove duplicates
        mentioned_colleges = list(set(mentioned_colleges))
        
        # Check for general query patterns
        is_general = any(re.search(pattern, question_lower) for pattern in self.general_patterns)
        
        # Determine query type
        if mentioned_colleges and not is_general:
            query_type = "college_specific"
        elif mentioned_colleges and is_general:
            query_type = "college_specific_general"  # e.g., "What is the admission process for IIT Bombay?"
        elif is_general and not mentioned_colleges:
            query_type = "general"
        else:
            query_type = "specific"  # Specific question but no college mentioned
        
        return {
            "type": query_type,
            "mentioned_colleges": mentioned_colleges,
            "is_general": is_general,
            "requires_clarification": query_type == "general"
        }
    
    def generate_general_response(self, question: str, classification: Dict) -> Dict:
        """Generate appropriate response for general queries"""
        question_lower = question.lower()
        
        # Common general responses
        if "admission" in question_lower or "apply" in question_lower:
            return {
                "type": "general_guidance",
                "answer": """To apply for engineering college admissions in India for 2025-26:

**For IITs, NITs, IIITs:**
• JEE Main 2025: Session 1 (Jan 24 - Feb 1), Session 2 (Apr 1 - Apr 8)
• JEE Advanced 2025: May 18, 2025
• Apply through JoSAA counseling (June-September 2025)

**For State Colleges:**
• Apply through respective state entrance exams
• Some accept JEE Main scores

**For Private Colleges:**
• Direct applications or entrance tests
• Some accept JEE Main scores

**General Process:**
1. Check eligibility criteria
2. Register for entrance exams
3. Fill application forms
4. Submit required documents
5. Participate in counseling

*Please specify which college you're interested in for detailed information.*""",
                "confidence": 95.0,
                "college": "General Information",
                "category": "Admissions"
            }
        
        elif "fees" in question_lower or "cost" in question_lower:
            return {
                "type": "general_guidance", 
                "answer": """Engineering College Fee Structure in India (2025-26):

**Government Colleges:**
• IITs: ₹4,00,000 per year (including hostel)
• NITs: ₹2,50,000 per year (including hostel)
• State Government: ₹1,00,000 - ₹1,50,000 per year

**Private Colleges:**
• Tier 1 Private: ₹3,00,000 - ₹4,50,000 per year
• Tier 2 Private: ₹2,00,000 - ₹3,00,000 per year

**Additional Costs:**
• Hostel (if separate): ₹50,000 - ₹1,00,000 per year
• Books & Materials: ₹20,000 - ₹30,000 per year

*Fees vary significantly by college. Please specify which college for exact fee structure.*""",
                "confidence": 95.0,
                "college": "General Information",
                "category": "Fees"
            }
        
        elif "placement" in question_lower or "package" in question_lower:
            return {
                "type": "general_guidance",
                "answer": """Engineering Placement Statistics in India (2024-25):

**IITs:** Average ₹15-25 LPA, Highest ₹50+ LPA
**NITs:** Average ₹8-15 LPA, Highest ₹30+ LPA  
**IIITs:** Average ₹10-18 LPA, Highest ₹40+ LPA
**Top Private:** Average ₹6-12 LPA, Highest ₹25+ LPA
**Other Private:** Average ₹3-8 LPA, Highest ₹15+ LPA

**Top Recruiters:**
• IT: TCS, Infosys, Wipro, Accenture, Cognizant
• Product: Google, Microsoft, Amazon, Adobe
• Core: L&T, BHEL, ONGC, BARC, ISRO

**Factors Affecting Placements:**
• College reputation & ranking
• Student's academic performance
• Technical skills & certifications
• Interview preparation

*Please specify which college for detailed placement statistics.*""",
                "confidence": 95.0,
                "college": "General Information", 
                "category": "Placements"
            }
        
        else:
            # Default general response
            return {
                "type": "clarification_needed",
                "answer": f"""I can help you with information about engineering colleges in India. However, your question "{question}" is quite general. 

I have detailed information about 637+ engineering colleges including:
• Admission processes and requirements
• Fee structures and scholarships  
• Placement statistics and companies
• Campus facilities and infrastructure
• Course details and curriculum

**Please specify:**
• Which college are you interested in? (e.g., IIT Bombay, NIT Trichy, etc.)
• Or would you like general information about a category? (e.g., all IITs, top private colleges)

This will help me provide you with accurate and specific information.""",
                "confidence": 90.0,
                "college": "Clarification Required",
                "category": "General"
            }
    
    def query(self, question: str, top_k: int = 5) -> List[Dict]:
        """Enhanced query processing with intelligent classification"""
        
        # Classify the query
        classification = self.classify_query(question)
        
        # Handle general queries
        if classification["requires_clarification"]:
            general_response = self.generate_general_response(question, classification)
            return [general_response]
        
        # Handle college-specific queries normally
        if self.embeddings is None:
            return self.fallback_search(question, top_k)
        
        # Create embedding for the question
        question_embedding = self.sentence_model.encode([question])
        faiss.normalize_L2(question_embedding)
        
        # Search for similar Q&A pairs
        scores, indices = self.index.search(question_embedding, top_k * 2)  # Get more results to filter
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.qa_pairs):
                qa = self.qa_pairs[idx]
                
                # Filter results based on classification
                if classification["type"] == "college_specific" and classification["mentioned_colleges"]:
                    # Only include results from mentioned colleges
                    if qa['college'] in classification["mentioned_colleges"]:
                        results.append({
                            'college': qa['college'],
                            'category': qa['category'],
                            'question': qa['question'],
                            'answer': qa['answer'],
                            'confidence': float(score) * 100
                        })
                else:
                    # Include all relevant results but boost confidence for exact matches
                    confidence = float(score) * 100
                    
                    # Boost confidence if college mentioned in query matches result
                    if classification["mentioned_colleges"]:
                        if qa['college'] in classification["mentioned_colleges"]:
                            confidence = min(confidence * 1.2, 100.0)  # Boost but cap at 100%
                    
                    results.append({
                        'college': qa['college'],
                        'category': qa['category'], 
                        'question': qa['question'],
                        'answer': qa['answer'],
                        'confidence': confidence
                    })
        
        # Sort by confidence and return top_k
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results[:top_k]
    
    def fallback_search(self, question: str, top_k: int = 5) -> List[Dict]:
        """Fallback search using simple text matching"""
        question_lower = question.lower()
        matches = []
        
        for qa in self.qa_pairs:
            score = 0
            qa_text = f"{qa['question']} {' '.join(qa.get('keywords', []))}".lower()
            
            # Simple keyword matching
            question_words = set(question_lower.split())
            qa_words = set(qa_text.split())
            
            # Calculate Jaccard similarity
            intersection = len(question_words.intersection(qa_words))
            union = len(question_words.union(qa_words))
            
            if union > 0:
                score = intersection / union
            
            if score > 0:
                matches.append({
                    'college': qa['college'],
                    'category': qa['category'],
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'confidence': score * 100
                })
        
        # Sort by score and return top_k
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches[:top_k]

def test_improved_agent():
    """Test the improved agent with various query types"""
    agent = ImprovedCollegeAI()
    
    test_queries = [
        "How to apply for admission in 2025?",  # General
        "What are the fees?",  # General
        "What is the fee at IIT Bombay?",  # College-specific
        "Which companies visit for placements?",  # General
        "What companies visit NIT Trichy for placements?",  # College-specific
        "Average package in private colleges",  # General
    ]
    
    print("\n🧪 Testing Improved Query Classification:")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        
        # Test classification
        classification = agent.classify_query(query)
        print(f"   Classification: {classification['type']}")
        if classification['mentioned_colleges']:
            print(f"   Mentioned Colleges: {classification['mentioned_colleges'][:3]}")
        
        # Test query results
        results = agent.query(query, top_k=2)
        print(f"   Results: {len(results)} answers")
        
        if results:
            best = results[0]
            print(f"   Best: {best['college']} ({best['confidence']:.1f}%)")
            print(f"   Answer: {best['answer'][:100]}...")

if __name__ == "__main__":
    test_improved_agent()
