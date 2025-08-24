#!/usr/bin/env python3
"""
Offline Dynamic College AI - No API Keys Required
Uses local models for translation and language detection
"""

import os
import json
import time
import pickle
import re
from pathlib import Path
from typing import Dict, List, Any
import hashlib
from datetime import datetime

# Offline language detection patterns
LANGUAGE_PATTERNS = {
    'hi': [r'[\u0900-\u097F]', r'(है|में|का|की|के|से|को|और|या|कि|कैसे|क्या|कहाँ|कब|कौन)'],
    'bn': [r'[\u0980-\u09FF]', r'(আছে|এর|এবং|কি|কিভাবে|কোথায়|কখন|কে|কেন)'],
    'te': [r'[\u0C00-\u0C7F]', r'(ఉంది|లో|మరియు|ఎలా|ఎక్కడ|ఎప్పుడు|ఎవరు|ఎందుకు)'],
    'ta': [r'[\u0B80-\u0BFF]', r'(உள்ளது|இல்|மற்றும்|எப்படி|எங்கே|எப்போது|யார்|ஏன்)'],
    'mr': [r'[\u0900-\u097F]', r'(आहे|मध्ये|आणि|कसे|कुठे|केव्हा|कोण|का)'],
    'gu': [r'[\u0A80-\u0AFF]', r'(છે|માં|અને|કેવી|ક્યાં|ક્યારે|કોણ|શા)'],
    'kn': [r'[\u0C80-\u0CFF]', r'(ಇದೆ|ನಲ್ಲಿ|ಮತ್ತು|ಹೇಗೆ|ಎಲ್ಲಿ|ಯಾವಾಗ|ಯಾರು|ಏಕೆ)'],
    'ml': [r'[\u0D00-\u0D7F]', r'(ഉണ്ട്|ൽ|ഒപ്പം|എങ്ങനെ|എവിടെ|എപ്പോൾ|ആര്|എന്തുകൊണ്ട്)'],
    'pa': [r'[\u0A00-\u0A7F]', r'(ਹੈ|ਵਿੱਚ|ਅਤੇ|ਕਿਵੇਂ|ਕਿੱਥੇ|ਕਦੋਂ|ਕੌਣ|ਕਿਉਂ)'],
    'or': [r'[\u0B00-\u0B7F]', r'(ଅଛି|ରେ|ଏବଂ|କିପରି|କେଉଁଠି|କେବେ|କିଏ|କାହିଁକି)'],
    'as': [r'[\u0980-\u09FF]', r'(আছে|ত|আৰু|কেনেকৈ|ক\'ত|কেতিয়া|কোন|কিয়)'],
    'ur': [r'[\u0600-\u06FF]', r'(ہے|میں|اور|کیسے|کہاں|کب|کون|کیوں)']
}

# Simple translation dictionary for common words
TRANSLATION_DICT = {
    'hi': {
        'fee': 'फीस', 'fees': 'फीस', 'cost': 'लागत', 'price': 'कीमत',
        'admission': 'प्रवेश', 'college': 'कॉलेज', 'university': 'विश्वविद्यालय',
        'placement': 'प्लेसमेंट', 'job': 'नौकरी', 'salary': 'वेतन',
        'course': 'कोर्स', 'engineering': 'इंजीनियरिंग', 'computer': 'कंप्यूटर',
        'what': 'क्या', 'how': 'कैसे', 'where': 'कहाँ', 'when': 'कब'
    },
    'bn': {
        'fee': 'ফি', 'fees': 'ফি', 'cost': 'খরচ', 'price': 'দাম',
        'admission': 'ভর্তি', 'college': 'কলেজ', 'university': 'বিশ্ববিদ্যালয়',
        'placement': 'চাকরি', 'job': 'কাজ', 'salary': 'বেতন',
        'course': 'কোর্স', 'engineering': 'প্রকৌশল', 'computer': 'কম্পিউটার',
        'what': 'কি', 'how': 'কিভাবে', 'where': 'কোথায়', 'when': 'কখন'
    },
    'te': {
        'fee': 'ఫీజు', 'fees': 'ఫీజులు', 'cost': 'ఖర్చు', 'price': 'ధర',
        'admission': 'ప్రవేశం', 'college': 'కాలేజీ', 'university': 'విశ్వవిద్యాలయం',
        'placement': 'ప్లేస్‌మెంట్', 'job': 'ఉద్యోగం', 'salary': 'జీతం',
        'course': 'కోర్సు', 'engineering': 'ఇంజనీరింగ్', 'computer': 'కంప్యూటర్',
        'what': 'ఏమిటి', 'how': 'ఎలా', 'where': 'ఎక్కడ', 'when': 'ఎప్పుడు'
    }
}

class OfflineTranslator:
    """Offline translator using local patterns and dictionaries"""
    
    def __init__(self):
        self.supported_languages = list(LANGUAGE_PATTERNS.keys()) + ['en']
        print("🔤 Offline translator initialized")
        print(f"🌐 Supported languages: {len(self.supported_languages)}")
    
    def detect_language(self, text: str) -> str:
        """Detect language using character patterns"""
        if not text.strip():
            return 'en'
        
        text_lower = text.lower()
        
        # Check for English first
        if re.search(r'^[a-zA-Z0-9\s\.,\?!]+$', text):
            return 'en'
        
        # Check each language pattern
        for lang_code, patterns in LANGUAGE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return lang_code
        
        return 'en'  # Default to English
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = 'auto') -> str:
        """Simple offline translation using word mapping"""
        if source_lang == 'auto':
            source_lang = self.detect_language(text)
        
        if source_lang == target_lang:
            return text
        
        # English to other languages
        if source_lang == 'en' and target_lang in TRANSLATION_DICT:
            return self._translate_en_to_lang(text, target_lang)
        
        # Other languages to English
        if target_lang == 'en' and source_lang in TRANSLATION_DICT:
            return self._translate_lang_to_en(text, source_lang)
        
        # If no translation available, return original
        return text
    
    def _translate_en_to_lang(self, text: str, target_lang: str) -> str:
        """Translate English to target language"""
        if target_lang not in TRANSLATION_DICT:
            return text
        
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            # Remove punctuation for lookup
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in TRANSLATION_DICT[target_lang]:
                translated_words.append(TRANSLATION_DICT[target_lang][clean_word])
            else:
                translated_words.append(word)
        
        return ' '.join(translated_words)
    
    def _translate_lang_to_en(self, text: str, source_lang: str) -> str:
        """Translate from source language to English"""
        if source_lang not in TRANSLATION_DICT:
            return text
        
        # Reverse lookup in translation dictionary
        reverse_dict = {v: k for k, v in TRANSLATION_DICT[source_lang].items()}
        
        words = text.split()
        translated_words = []
        
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in reverse_dict:
                translated_words.append(reverse_dict[clean_word])
            else:
                translated_words.append(word)
        
        return ' '.join(translated_words)

class OfflineDynamicCollegeAI:
    """Offline Dynamic College AI - No API Keys Required"""
    
    def __init__(self, base_model_path: str = "college_ai_rtx2050_trained.pkl"):
        self.base_model_path = base_model_path
        self.data_path = Path("college_data")
        self.cache_path = Path("dynamic_cache")
        self.cache_path.mkdir(exist_ok=True)
        
        # Initialize offline translator
        self.translator = OfflineTranslator()
        
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
        
        print("🔄 Offline Dynamic College AI initialized")
        print(f"📊 Base model: {len(self.base_agent.colleges_data) if self.base_agent else 0} colleges")
        print("🔒 No API keys required - fully offline!")
    
    def load_base_model(self):
        """Load the base trained model"""
        try:
            if Path(self.base_model_path).exists():
                with open(self.base_model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                # Create a simple agent-like object
                class SimpleAgent:
                    def __init__(self, data):
                        self.colleges_data = data.get('colleges_data', {})
                        self.qa_pairs = data.get('qa_pairs', [])
                        self.embeddings = data.get('embeddings')
                
                self.base_agent = SimpleAgent(model_data)
                print(f"✅ Base model loaded: {self.base_model_path}")
                return True
            else:
                print(f"❌ Base model not found: {self.base_model_path}")
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
                    file_key = json_file.stem
                    college_data[file_key] = data
            except Exception as e:
                print(f"⚠️  Error loading {json_file}: {e}")
        
        return college_data
    
    def has_college_data_changed(self, college_name: str, new_data: Dict):
        """Check if college data has changed"""
        if college_name not in self.base_agent.colleges_data:
            return True
        
        old_data = self.base_agent.colleges_data[college_name]
        
        old_str = json.dumps(old_data, sort_keys=True)
        new_str = json.dumps(new_data, sort_keys=True)
        
        return old_str != new_str
    
    def query_with_offline_translation(self, question: str, top_k: int = 5, target_language: str = None):
        """Query with offline translation and dynamic data"""
        # Detect language if not specified
        if target_language is None:
            target_language = self.translator.detect_language(question)
        
        print(f"🔍 Detected language: {target_language}")
        
        # Translate question to English for searching
        english_question = question
        if target_language != 'en':
            english_question = self.translator.translate_text(question, 'en', target_language)
            print(f"🔄 Translated query: {english_question}")
        
        # Check for data changes
        current_time = time.time()
        if current_time - self.last_scan_time > 60:  # Check every minute
            self.detect_data_changes()
            self.last_scan_time = current_time
        
        # Search in base model (simplified)
        base_results = self.search_base_model(english_question)
        
        # Search in new/updated data
        dynamic_results = self.search_dynamic_data(english_question)
        
        # Combine results
        all_results = base_results + dynamic_results
        
        # Sort by relevance
        all_results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        # Translate results back if needed
        if target_language != 'en':
            for result in all_results:
                result['answer'] = self.translator.translate_text(result['answer'], target_language, 'en')
                result['translated'] = True
        
        return all_results[:top_k]
    
    def search_base_model(self, question: str):
        """Simple search in base model data"""
        results = []
        question_lower = question.lower()
        
        # Simple keyword matching in Q&A pairs
        for qa in self.base_agent.qa_pairs[:100]:  # Limit for demo
            qa_text = f"{qa.get('question', '')} {qa.get('answer', '')}".lower()
            
            # Calculate simple relevance score
            score = 0
            question_words = question_lower.split()
            for word in question_words:
                if len(word) > 2 and word in qa_text:
                    score += 1
            
            if score > 0:
                results.append({
                    'college': qa.get('college', 'Unknown'),
                    'category': qa.get('category', 'general'),
                    'question': qa.get('question', ''),
                    'answer': qa.get('answer', ''),
                    'confidence': min(score * 20, 95),
                    'source': 'base'
                })
        
        return sorted(results, key=lambda x: x['confidence'], reverse=True)[:5]
    
    def search_dynamic_data(self, question: str):
        """Search in new/updated college data"""
        results = []
        question_lower = question.lower()
        
        # Search new colleges
        for college_name, college_data in self.new_colleges.items():
            score = self.calculate_relevance_score(question_lower, college_data)
            if score > 0.3:
                answer = self.generate_answer_from_data(question, college_data)
                
                results.append({
                    'college': f"🆕 {college_name}",
                    'category': 'general',
                    'question': question,
                    'answer': answer,
                    'confidence': min(score * 100, 95),
                    'source': 'dynamic'
                })
        
        # Search updated colleges
        for college_name, college_data in self.updated_colleges.items():
            score = self.calculate_relevance_score(question_lower, college_data)
            if score > 0.3:
                answer = self.generate_answer_from_data(question, college_data)
                
                results.append({
                    'college': f"🔄 {college_name}",
                    'category': 'general',
                    'question': question,
                    'answer': answer,
                    'confidence': min(score * 100, 95),
                    'source': 'dynamic'
                })
        
        return results
    
    def calculate_relevance_score(self, question: str, college_data: Dict):
        """Calculate relevance score for college data"""
        score = 0.0
        question_words = question.split()
        
        searchable_text = json.dumps(college_data, ensure_ascii=False).lower()
        
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
        if 'fee' in question.lower():
            if 'basic_info' in college_data and 'fees' in str(college_data['basic_info']).lower():
                return f"Fee information: {str(college_data.get('basic_info', {}))[:200]}..."
        
        if 'placement' in question.lower():
            if 'placements' in college_data:
                return f"Placement details: {str(college_data.get('placements', {}))[:200]}..."
        
        if 'admission' in question.lower():
            if 'admissions' in college_data:
                return f"Admission information: {str(college_data.get('admissions', {}))[:200]}..."
        
        return f"Information available: {str(college_data)[:200]}..."

def main():
    """Demo of offline dynamic system"""
    print("🚀 Offline Dynamic College AI - No API Keys!")
    print("=" * 60)
    
    ai = OfflineDynamicCollegeAI()
    
    if not ai.base_agent:
        print("❌ Base model not available. Please train first:")
        print("   python train_rtx2050_gpu.py")
        return
    
    print(f"\n🎮 Interactive Mode - Ask questions in any language!")
    print("🔒 Fully offline - no internet or API keys required")
    print("Type 'quit' to exit")
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if query.lower() in ['quit', 'exit']:
                break
            
            if not query:
                continue
            
            print("🔍 Processing offline...")
            results = ai.query_with_offline_translation(query, top_k=3)
            
            if results:
                for i, result in enumerate(results, 1):
                    source_icon = "🆕" if result.get('source') == 'dynamic' else "📚"
                    print(f"\n{i}. {source_icon} {result['college']} ({result['confidence']:.1f}%)")
                    print(f"   💡 {result['answer'][:150]}...")
                    if result.get('translated'):
                        print(f"   🔄 Answer translated offline")
            else:
                print("❌ No results found")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
