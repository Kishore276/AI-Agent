#!/usr/bin/env python3
"""
Dynamic College AI Agent - Auto-updates without retraining
Automatically detects and incorporates new college data
"""

import os
import json
import time
import pickle
from pathlib import Path
from typing import Dict, List, Any
import hashlib
from datetime import datetime

class DynamicCollegeAI:
    """Dynamic AI Agent that auto-updates with new data"""
    
    def __init__(self, base_model_path: str = "college_ai_rtx2050_trained.pkl"):
        self.base_model_path = base_model_path
        self.data_path = Path("college_data")
        self.cache_path = Path("dynamic_cache")
        self.cache_path.mkdir(exist_ok=True)
        
        # Load base trained model
        self.base_agent = None
        self.load_base_model()
        
        # Dynamic data tracking
        self.data_hash_file = self.cache_path / "data_hash.json"
        self.new_data_cache = self.cache_path / "new_data.json"
        self.last_scan_time = 0
        
        # Initialize data monitoring
        self.current_data_hash = self.calculate_data_hash()
        self.new_colleges = {}
        self.updated_colleges = {}
        
        print("🔄 Dynamic College AI initialized")
        print(f"📊 Base model: {len(self.base_agent.colleges_data) if self.base_agent else 0} colleges")
        
    def load_base_model(self):
        """Load the base trained model"""
        try:
            from train_college_ai_agent import CollegeAIAgent
            
            if Path(self.base_model_path).exists():
                self.base_agent = CollegeAIAgent(enable_multilingual=True)
                success = self.base_agent.load_model(self.base_model_path)
                
                if success:
                    print(f"✅ Base model loaded: {self.base_model_path}")
                    return True
                else:
                    print(f"❌ Failed to load base model")
                    return False
            else:
                print(f"❌ Base model not found: {self.base_model_path}")
                print("🔄 Please train the base model first")
                return False
                
        except Exception as e:
            print(f"❌ Error loading base model: {e}")
            return False
    
    def calculate_data_hash(self):
        """Calculate hash of all college data for change detection"""
        if not self.data_path.exists():
            return ""
        
        all_files_content = []
        
        for college_dir in sorted(self.data_path.iterdir()):
            if college_dir.is_dir():
                for json_file in sorted(college_dir.glob("*.json")):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            all_files_content.append(f"{json_file.name}:{content}")
                    except Exception:
                        continue
        
        combined_content = "".join(all_files_content)
        return hashlib.md5(combined_content.encode()).hexdigest()
    
    def detect_data_changes(self):
        """Detect if college data has been updated"""
        new_hash = self.calculate_data_hash()
        
        # Load previous hash
        previous_hash = ""
        if self.data_hash_file.exists():
            try:
                with open(self.data_hash_file, 'r') as f:
                    hash_data = json.load(f)
                    previous_hash = hash_data.get('hash', '')
            except Exception:
                pass
        
        # Check for changes
        if new_hash != previous_hash:
            print(f"🔄 Data changes detected!")
            self.scan_for_new_data()
            
            # Update hash file
            with open(self.data_hash_file, 'w') as f:
                json.dump({
                    'hash': new_hash,
                    'last_update': datetime.now().isoformat(),
                    'scan_time': time.time()
                }, f, indent=2)
            
            return True
        
        return False
    
    def scan_for_new_data(self):
        """Scan for new or updated college data"""
        print("🔍 Scanning for new college data...")
        
        if not self.base_agent:
            print("❌ Base model not available")
            return
        
        existing_colleges = set(self.base_agent.colleges_data.keys())
        current_colleges = set()
        
        new_data = {
            'new_colleges': {},
            'updated_colleges': {},
            'scan_time': time.time()
        }
        
        # Scan all college directories
        for college_dir in self.data_path.iterdir():
            if college_dir.is_dir():
                college_name = college_dir.name
                current_colleges.add(college_name)
                
                # Load college data
                college_data = self.load_college_data(college_dir)
                
                if college_name not in existing_colleges:
                    # New college found
                    print(f"🆕 New college: {college_name}")
                    new_data['new_colleges'][college_name] = college_data
                else:
                    # Check if existing college data changed
                    if self.has_college_data_changed(college_name, college_data):
                        print(f"🔄 Updated college: {college_name}")
                        new_data['updated_colleges'][college_name] = college_data
        
        # Save new data cache
        with open(self.new_data_cache, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        
        self.new_colleges = new_data['new_colleges']
        self.updated_colleges = new_data['updated_colleges']
        
        total_changes = len(self.new_colleges) + len(self.updated_colleges)
        print(f"✅ Scan complete: {len(self.new_colleges)} new, {len(self.updated_colleges)} updated")
        
        return total_changes > 0
    
    def load_college_data(self, college_dir: Path):
        """Load all data for a college"""
        college_data = {}
        
        for json_file in college_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    file_key = json_file.stem  # filename without extension
                    college_data[file_key] = data
            except Exception as e:
                print(f"⚠️  Error loading {json_file}: {e}")
        
        return college_data
    
    def has_college_data_changed(self, college_name: str, new_data: Dict):
        """Check if college data has changed"""
        if college_name not in self.base_agent.colleges_data:
            return True
        
        old_data = self.base_agent.colleges_data[college_name]
        
        # Simple comparison - you can make this more sophisticated
        old_str = json.dumps(old_data, sort_keys=True)
        new_str = json.dumps(new_data, sort_keys=True)
        
        return old_str != new_str
    
    def generate_qa_for_new_data(self, college_name: str, college_data: Dict):
        """Generate Q&A pairs for new college data"""
        qa_pairs = []
        
        # Use the same Q&A generation logic as the base model
        if hasattr(self.base_agent, 'generate_synthetic_qa'):
            new_qa = self.base_agent.generate_synthetic_qa(college_name, college_data)
            qa_pairs.extend(new_qa)
        
        return qa_pairs
    
    def query_with_dynamic_data(self, question: str, top_k: int = 5, target_language: str = None):
        """Query with automatic inclusion of new data"""
        # Check for data changes (lightweight check)
        current_time = time.time()
        if current_time - self.last_scan_time > 60:  # Check every minute
            self.detect_data_changes()
            self.last_scan_time = current_time
        
        # First, try base model
        base_results = []
        if self.base_agent:
            try:
                base_results = self.base_agent.query_agent(question, top_k, target_language)
            except Exception as e:
                print(f"⚠️  Base model query failed: {e}")
        
        # Search in new/updated data
        dynamic_results = self.search_dynamic_data(question, target_language)
        
        # Combine and rank results
        all_results = base_results + dynamic_results
        
        # Sort by confidence and return top_k
        all_results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        # Add dynamic data indicator
        for result in all_results:
            if result.get('source') == 'dynamic':
                result['college'] = f"🆕 {result['college']}"
        
        return all_results[:top_k]
    
    def search_dynamic_data(self, question: str, target_language: str = None):
        """Search in new/updated college data"""
        results = []
        
        # Simple keyword-based search for new data
        question_lower = question.lower()
        
        # Search new colleges
        for college_name, college_data in self.new_colleges.items():
            score = self.calculate_relevance_score(question_lower, college_data)
            if score > 0.3:  # Threshold for relevance
                answer = self.generate_answer_from_data(question, college_data)
                
                results.append({
                    'rank': len(results) + 1,
                    'score': score,
                    'college': college_name,
                    'category': 'general',
                    'question': question,
                    'answer': answer,
                    'confidence': min(score * 100, 95),
                    'source': 'dynamic',
                    'language': target_language or 'en'
                })
        
        # Search updated colleges
        for college_name, college_data in self.updated_colleges.items():
            score = self.calculate_relevance_score(question_lower, college_data)
            if score > 0.3:
                answer = self.generate_answer_from_data(question, college_data)
                
                results.append({
                    'rank': len(results) + 1,
                    'score': score,
                    'college': f"Updated: {college_name}",
                    'category': 'general',
                    'question': question,
                    'answer': answer,
                    'confidence': min(score * 100, 95),
                    'source': 'dynamic',
                    'language': target_language or 'en'
                })
        
        return results
    
    def calculate_relevance_score(self, question: str, college_data: Dict):
        """Calculate relevance score for college data"""
        score = 0.0
        question_words = question.split()
        
        # Convert college data to searchable text
        searchable_text = json.dumps(college_data, ensure_ascii=False).lower()
        
        # Simple keyword matching
        for word in question_words:
            if len(word) > 2 and word in searchable_text:
                score += 0.1
        
        # Boost for specific keywords
        if 'fee' in question and ('fee' in searchable_text or 'cost' in searchable_text):
            score += 0.3
        if 'placement' in question and 'placement' in searchable_text:
            score += 0.3
        if 'admission' in question and 'admission' in searchable_text:
            score += 0.3
        
        return min(score, 1.0)
    
    def generate_answer_from_data(self, question: str, college_data: Dict):
        """Generate answer from college data"""
        # Simple answer generation - can be made more sophisticated
        if 'fee' in question.lower():
            if 'basic_info' in college_data and 'fees' in str(college_data['basic_info']).lower():
                return f"Fee information: {str(college_data.get('basic_info', {}))[:200]}..."
        
        if 'placement' in question.lower():
            if 'placements' in college_data:
                return f"Placement details: {str(college_data.get('placements', {}))[:200]}..."
        
        if 'admission' in question.lower():
            if 'admissions' in college_data:
                return f"Admission information: {str(college_data.get('admissions', {}))[:200]}..."
        
        # Default answer
        return f"Information available about this college: {str(college_data)[:200]}..."
    
    def get_status(self):
        """Get current status of dynamic system"""
        return {
            'base_model_loaded': self.base_agent is not None,
            'base_colleges': len(self.base_agent.colleges_data) if self.base_agent else 0,
            'new_colleges': len(self.new_colleges),
            'updated_colleges': len(self.updated_colleges),
            'last_scan': self.last_scan_time,
            'data_hash': self.current_data_hash[:8]  # First 8 chars
        }

def main():
    """Demo of dynamic college AI"""
    print("🚀 Dynamic College AI Agent Demo")
    print("=" * 50)
    
    # Initialize dynamic AI
    ai = DynamicCollegeAI()
    
    if not ai.base_agent:
        print("❌ Base model not available. Please train first:")
        print("   python train_rtx2050_gpu.py")
        return
    
    # Show status
    status = ai.get_status()
    print(f"\n📊 System Status:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Interactive mode
    print(f"\n🎮 Interactive Mode - Ask questions!")
    print("System will automatically detect and use new college data")
    print("Type 'quit' to exit, 'scan' to force data scan")
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if query.lower() in ['quit', 'exit']:
                break
            
            if query.lower() == 'scan':
                ai.detect_data_changes()
                continue
            
            if not query:
                continue
            
            print("🔍 Searching (including new data)...")
            results = ai.query_with_dynamic_data(query, top_k=3)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. 🎯 {result['college']} ({result['confidence']:.1f}%)")
                    print(f"   💡 {result['answer'][:150]}...")
                    if result.get('source') == 'dynamic':
                        print(f"   🆕 From new/updated data")
            else:
                print("❌ No results found")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
