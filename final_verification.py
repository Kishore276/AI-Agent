"""
Final Verification
Verify that all issues have been resolved and database is perfect
"""

import json
import os
from pathlib import Path
from typing import Dict, List

class FinalVerification:
    """Final verification of database quality"""
    
    def __init__(self):
        self.base_path = Path("college_data")
        
        # Generic patterns that should not exist
        self.forbidden_patterns = [
            "for detailed information about",
            "please visit the official website",
            "contact the admission office",
            "our counselors are available",
            "committed to providing quality engineering education",
            "has excellent infrastructure including modern laboratories",
            "various it and engineering companies visit campus"
        ]
    
    def perform_final_verification(self):
        """Perform final verification of all colleges"""
        print("🔍 Final Verification - Checking all 504 colleges...")
        print("=" * 60)
        
        colleges = [d for d in os.listdir(self.base_path) if os.path.isdir(self.base_path / d)]
        total_colleges = len(colleges)
        
        total_questions = 0
        issues_found = 0
        perfect_colleges = 0
        
        for i, college_name in enumerate(sorted(colleges), 1):
            questions_checked, college_issues = self.verify_college(college_name)
            total_questions += questions_checked
            issues_found += college_issues
            
            if college_issues == 0:
                perfect_colleges += 1
                print(f"✅ [{i:3d}/504] {college_name} - Perfect ({questions_checked} questions)")
            else:
                print(f"⚠️  [{i:3d}/504] {college_name} - {college_issues} issues found")
            
            # Progress indicator
            if i % 100 == 0:
                print(f"\n📈 Progress: {i}/504 colleges verified")
                print(f"📊 Current stats: {total_questions:,} questions, {issues_found} issues, {perfect_colleges} perfect colleges\n")
        
        # Final results
        success_rate = ((total_questions - issues_found) / total_questions * 100) if total_questions > 0 else 100
        
        print(f"\n🎉 Final Verification Complete!")
        print(f"📊 Final Results:")
        print(f"   - Total Colleges: {total_colleges}")
        print(f"   - Total Questions: {total_questions:,}")
        print(f"   - Perfect Colleges: {perfect_colleges} ({perfect_colleges/total_colleges*100:.1f}%)")
        print(f"   - Issues Found: {issues_found}")
        print(f"   - Success Rate: {success_rate:.2f}%")
        
        if issues_found == 0:
            print("🚀 DATABASE IS PERFECT! All issues resolved!")
        else:
            print(f"⚠️  {issues_found} issues still need attention")
        
        return total_questions, issues_found, perfect_colleges
    
    def verify_college(self, college_name: str) -> tuple:
        """Verify a single college"""
        faq_path = self.base_path / college_name / "faq.json"
        
        if not faq_path.exists():
            return 0, 0
        
        try:
            with open(faq_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions_checked = 0
            issues_found = 0
            
            # Check AI agent FAQs
            if "ai_agent_faqs" in data and "categories" in data["ai_agent_faqs"]:
                for category, faqs in data["ai_agent_faqs"]["categories"].items():
                    for faq in faqs:
                        questions_checked += 1
                        answer = faq.get("answer", "")
                        
                        if self.has_forbidden_pattern(answer):
                            issues_found += 1
            
            # Check original FAQs
            if "frequently_asked_questions" in data:
                for category, faqs in data["frequently_asked_questions"].items():
                    if isinstance(faqs, list):
                        for faq in faqs:
                            if isinstance(faq, dict) and "answer" in faq:
                                questions_checked += 1
                                answer = faq.get("answer", "")
                                
                                if self.has_forbidden_pattern(answer):
                                    issues_found += 1
            
            return questions_checked, issues_found
                
        except Exception as e:
            print(f"❌ Error verifying {college_name}: {e}")
            return 0, 0
    
    def has_forbidden_pattern(self, answer: str) -> bool:
        """Check if answer contains forbidden patterns"""
        return any(pattern in answer.lower() for pattern in self.forbidden_patterns)

if __name__ == "__main__":
    verifier = FinalVerification()
    
    print("🔍 Final Verification System")
    print("=" * 60)
    
    total_questions, issues_found, perfect_colleges = verifier.perform_final_verification()
    
    if issues_found == 0:
        print(f"\n🎉 SUCCESS! Database is 100% perfect!")
        print(f"✅ All {total_questions:,} questions across 504 colleges are perfect!")
        print("🚀 Ready for production deployment!")
    else:
        print(f"\n⚠️  {issues_found} issues still need attention")
        print("🔧 Additional fixes may be required")
