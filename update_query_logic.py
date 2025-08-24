#!/usr/bin/env python3
"""
Update Main Training Agent with Improved Query Logic
Integrate intelligent query classification into the main agent
"""

import os
import shutil
from pathlib import Path

def backup_original_file():
    """Backup the original training agent"""
    original = "train_college_ai_agent.py"
    backup = "train_college_ai_agent_backup.py"
    
    if os.path.exists(original) and not os.path.exists(backup):
        shutil.copy2(original, backup)
        print(f"✅ Created backup: {backup}")

def update_training_agent():
    """Update the main training agent with improved query logic"""
    print("🔧 Updating main training agent with improved query classification...")
    
    # Read the current training agent
    with open("train_college_ai_agent.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add the improved query logic
    improved_query_method = '''
    def classify_query(self, question: str) -> Dict[str, any]:
        """Classify if query is general or college-specific"""
        question_lower = question.lower()
        
        # General query patterns
        general_patterns = [
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
        ]
        
        # Check for college-specific keywords
        mentioned_colleges = []
        college_keywords = list(self.colleges_data.keys())
        
        for college_name in college_keywords:
            if any(word.lower() in question_lower for word in college_name.split() if len(word) > 3):
                mentioned_colleges.append(college_name)
        
        # Check for general query patterns
        import re
        is_general = any(re.search(pattern, question_lower) for pattern in general_patterns)
        
        # Determine query type
        if mentioned_colleges and not is_general:
            query_type = "college_specific"
        elif mentioned_colleges and is_general:
            query_type = "college_specific_general"
        elif is_general and not mentioned_colleges:
            query_type = "general"
        else:
            query_type = "specific"
        
        return {
            "type": query_type,
            "mentioned_colleges": mentioned_colleges,
            "is_general": is_general,
            "requires_clarification": query_type == "general"
        }
    
    def generate_general_response(self, question: str) -> Dict:
        """Generate appropriate response for general queries"""
        question_lower = question.lower()
        
        if "admission" in question_lower or "apply" in question_lower:
            return {
                "college": "General Information",
                "category": "Admissions",
                "question": question,
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
                "confidence": 95.0
            }
        
        elif "fees" in question_lower or "cost" in question_lower:
            return {
                "college": "General Information",
                "category": "Fees", 
                "question": question,
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
                "confidence": 95.0
            }
        
        elif "placement" in question_lower or "package" in question_lower:
            return {
                "college": "General Information",
                "category": "Placements",
                "question": question,
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

*Please specify which college for detailed placement statistics.*""",
                "confidence": 95.0
            }
        
        else:
            return {
                "college": "Clarification Required",
                "category": "General",
                "question": question,
                "answer": f"""I can help you with information about engineering colleges in India. However, your question "{question}" is quite general. 

I have detailed information about 637+ engineering colleges including:
• Admission processes and requirements
• Fee structures and scholarships  
• Placement statistics and companies
• Campus facilities and infrastructure

**Please specify:**
• Which college are you interested in? (e.g., IIT Bombay, NIT Trichy, etc.)
• Or would you like general information about a category?

This will help me provide you with accurate and specific information.""",
                "confidence": 90.0
            }
'''
    
    # Find where to insert the new methods (before the query_agent method)
    query_agent_pos = content.find("def query_agent(self, question: str")
    
    if query_agent_pos != -1:
        # Insert the new methods before query_agent
        updated_content = (content[:query_agent_pos] + 
                          improved_query_method + 
                          "\n    " + 
                          content[query_agent_pos:])
        
        # Now update the query_agent method to use classification
        old_query_method = '''def query_agent(self, question: str, top_k: int = 5, target_language: str = None) -> List[Dict]:
        """Query the AI agent with a question in any supported language"""
        if not HAS_ML_LIBS:
            return self.fallback_search(question, top_k)

        # Detect language if not specified
        if target_language is None and self.translator:
            try:
                detected_lang = self.translator.detect_language(question)
                target_language = detected_lang if detected_lang != 'unknown' else 'en'
            except:
                target_language = 'en'

        # Use English embeddings for now (multilingual embeddings can be added later)
        if self.embeddings is None:
            return self.fallback_search(question, top_k)

        # Create embedding for the question
        question_embedding = self.sentence_model.encode([question])

        # Normalize for cosine similarity
        if HAS_ML_LIBS:
            import faiss
            faiss.normalize_L2(question_embedding)

        # Search for similar Q&A pairs
        scores, indices = self.index.search(question_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.qa_pairs):
                qa = self.qa_pairs[idx]
                
                # Translate if needed
                answer = qa['answer']
                if target_language and target_language != 'en' and self.translator:
                    try:
                        answer = self.translator.translate_text(answer, target_language)
                    except:
                        pass  # Keep original if translation fails
                
                results.append({
                    'college': qa['college'],
                    'category': qa['category'],
                    'question': qa['question'],
                    'answer': answer,
                    'confidence': float(score) * 100,
                    'language': target_language,
                    'translated': target_language != 'en'
                })

        return results'''
        
        new_query_method = '''def query_agent(self, question: str, top_k: int = 5, target_language: str = None) -> List[Dict]:
        """Enhanced query processing with intelligent classification"""
        
        # Classify the query first
        classification = self.classify_query(question)
        
        # Handle general queries with specific responses
        if classification["requires_clarification"]:
            general_response = self.generate_general_response(question)
            return [general_response]
        
        if not HAS_ML_LIBS:
            return self.fallback_search(question, top_k)

        # Detect language if not specified
        if target_language is None and self.translator:
            try:
                detected_lang = self.translator.detect_language(question)
                target_language = detected_lang if detected_lang != 'unknown' else 'en'
            except:
                target_language = 'en'

        # Use English embeddings for now
        if self.embeddings is None:
            return self.fallback_search(question, top_k)

        # Create embedding for the question
        question_embedding = self.sentence_model.encode([question])

        # Normalize for cosine similarity
        if HAS_ML_LIBS:
            import faiss
            faiss.normalize_L2(question_embedding)

        # Search for similar Q&A pairs
        scores, indices = self.index.search(question_embedding, top_k * 2)  # Get more to filter

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.qa_pairs):
                qa = self.qa_pairs[idx]
                
                # Filter based on classification
                include_result = True
                confidence_boost = 1.0
                
                if classification["type"] == "college_specific" and classification["mentioned_colleges"]:
                    # Only include results from mentioned colleges
                    if qa['college'] not in classification["mentioned_colleges"]:
                        include_result = False
                    else:
                        confidence_boost = 1.2  # Boost confidence for exact matches
                
                if include_result:
                    # Translate if needed
                    answer = qa['answer']
                    if target_language and target_language != 'en' and self.translator:
                        try:
                            answer = self.translator.translate_text(answer, target_language)
                        except:
                            pass  # Keep original if translation fails
                    
                    confidence = min(float(score) * 100 * confidence_boost, 100.0)
                    
                    results.append({
                        'college': qa['college'],
                        'category': qa['category'],
                        'question': qa['question'],
                        'answer': answer,
                        'confidence': confidence,
                        'language': target_language,
                        'translated': target_language != 'en'
                    })

        # Sort by confidence and return top_k
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results[:top_k]'''
        
        # Replace the old method with the new one
        updated_content = updated_content.replace(old_query_method, new_query_method)
        
        # Write the updated content
        with open("train_college_ai_agent.py", 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Updated train_college_ai_agent.py with improved query logic")
        return True
    else:
        print("❌ Could not find query_agent method to update")
        return False

def regenerate_models():
    """Regenerate models with improved query logic"""
    print("\n🔄 Regenerating models with improved query logic...")
    
    try:
        from train_college_ai_agent import CollegeAIAgent
        
        # Create improved agent
        agent = CollegeAIAgent(enable_multilingual=False)
        
        # Create embeddings
        agent.create_embeddings()
        
        # Save improved model
        agent.save_model("college_ai_agent_improved.pkl")
        
        # Replace the old model
        if os.path.exists("college_ai_agent.pkl"):
            os.rename("college_ai_agent.pkl", "college_ai_agent_old.pkl")
        os.rename("college_ai_agent_improved.pkl", "college_ai_agent.pkl")
        
        print("✅ Generated improved model with better query classification")
        return True
        
    except Exception as e:
        print(f"❌ Error regenerating models: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Updating AI Agent with Improved Query Logic")
    print("=" * 50)
    
    # Step 1: Backup original
    backup_original_file()
    
    # Step 2: Update training agent
    if update_training_agent():
        print("✅ Training agent updated successfully")
        
        # Step 3: Regenerate models
        if regenerate_models():
            print("✅ Models regenerated successfully")
            print("\n🎉 Update completed! The AI agent now handles general vs specific queries intelligently.")
        else:
            print("⚠️ Model regeneration failed, but code update successful")
    else:
        print("❌ Failed to update training agent")
