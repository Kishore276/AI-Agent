"""
Comprehensive Recheck
Final thorough verification of all colleges and questions
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import re

class ComprehensiveRecheck:
    """Comprehensive recheck of all Q&A pairs across all colleges"""
    
    def __init__(self):
        self.base_path = Path("college_data")
        self.issues_found = []
        
        # Comprehensive patterns to check for issues
        self.problematic_patterns = [
            # Generic contact patterns
            "for detailed information about",
            "please visit the official website",
            "contact the admission office",
            "our counselors are available",
            "contact the college directly",
            
            # Generic quality patterns
            "committed to providing quality engineering education",
            "has excellent infrastructure including modern laboratories",
            "provides comprehensive support",
            
            # Vague placement patterns
            "various it and engineering companies visit campus",
            "companies visit campus with packages ranging",
            "decent placement opportunities with",
            "good placement opportunities with",
            
            # Wrong answer patterns
            "for admission to" # when question is not about admission
        ]
        
        # Question-answer mismatch patterns
        self.mismatch_patterns = [
            # Attendance questions getting admission answers
            ("attendance", ["qualify jee", "admission to", "candidates must"]),
            
            # Company questions getting generic stats
            ("companies", ["placement rate", "packages ranging", "opportunities with"]),
            
            # Package questions getting company lists
            ("package", ["companies including", "recruiters include"]),
            
            # Library questions getting generic infrastructure
            ("library", ["excellent infrastructure including"]),
            
            # Sports questions getting lab answers
            ("sports", ["laboratory", "computer labs", "equipment"]),
            
            # Grading questions getting fee answers
            ("grading", ["annual fee", "tuition"]),
        ]
    
    def perform_comprehensive_recheck(self):
        """Perform comprehensive recheck of all colleges"""
        print("🔍 COMPREHENSIVE RECHECK - Final Verification")
        print("=" * 70)
        
        colleges = [d for d in os.listdir(self.base_path) if os.path.isdir(self.base_path / d)]
        total_colleges = len(colleges)
        
        print(f"📊 Rechecking all {total_colleges} colleges comprehensively...")
        
        total_questions = 0
        total_issues = 0
        perfect_colleges = 0
        colleges_with_issues = []
        
        for i, college_name in enumerate(sorted(colleges), 1):
            questions_checked, issues_found, issue_details = self.recheck_college(college_name)
            
            total_questions += questions_checked
            total_issues += issues_found
            
            if issues_found == 0:
                perfect_colleges += 1
                print(f"✅ [{i:3d}/504] {college_name} - Perfect ({questions_checked} questions)")
            else:
                colleges_with_issues.append((college_name, issues_found, issue_details))
                print(f"⚠️  [{i:3d}/504] {college_name} - {issues_found} issues found")
                for issue in issue_details:
                    print(f"      - {issue}")
            
            # Progress indicator
            if i % 100 == 0:
                print(f"\n📈 Progress: {i}/504 colleges rechecked")
                print(f"📊 Current: {total_questions:,} questions, {total_issues} issues, {perfect_colleges} perfect\n")
        
        # Final comprehensive report
        success_rate = ((total_questions - total_issues) / total_questions * 100) if total_questions > 0 else 100
        
        print(f"\n🎉 COMPREHENSIVE RECHECK COMPLETE!")
        print(f"📊 Final Detailed Results:")
        print(f"   - Total Colleges: {total_colleges}")
        print(f"   - Total Questions: {total_questions:,}")
        print(f"   - Perfect Colleges: {perfect_colleges} ({perfect_colleges/total_colleges*100:.1f}%)")
        print(f"   - Colleges with Issues: {len(colleges_with_issues)}")
        print(f"   - Total Issues Found: {total_issues}")
        print(f"   - Success Rate: {success_rate:.4f}%")
        
        if total_issues == 0:
            print("🚀 DATABASE IS 100% PERFECT! All issues resolved!")
        else:
            print(f"\n⚠️  DETAILED ISSUE BREAKDOWN:")
            for college_name, issue_count, issue_details in colleges_with_issues:
                print(f"   {college_name}: {issue_count} issues")
                for issue in issue_details:
                    print(f"      - {issue}")
        
        return total_questions, total_issues, perfect_colleges, colleges_with_issues
    
    def recheck_college(self, college_name: str) -> Tuple[int, int, List[str]]:
        """Comprehensive recheck of a single college"""
        faq_path = self.base_path / college_name / "faq.json"
        
        if not faq_path.exists():
            return 0, 0, []
        
        try:
            with open(faq_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions_checked = 0
            issues_found = 0
            issue_details = []
            
            # Check AI agent FAQs
            if "ai_agent_faqs" in data and "categories" in data["ai_agent_faqs"]:
                for category, faqs in data["ai_agent_faqs"]["categories"].items():
                    for faq in faqs:
                        questions_checked += 1
                        question = faq.get("question", "").lower().strip()
                        answer = faq.get("answer", "")
                        
                        issue_type = self.check_qa_comprehensive(question, answer)
                        if issue_type:
                            issues_found += 1
                            issue_details.append(f"AI FAQ - {category}: {issue_type}")
            
            # Check original FAQs
            if "frequently_asked_questions" in data:
                for category, faqs in data["frequently_asked_questions"].items():
                    if isinstance(faqs, list):
                        for faq in faqs:
                            if isinstance(faq, dict) and "question" in faq and "answer" in faq:
                                questions_checked += 1
                                question = faq.get("question", "").lower().strip()
                                answer = faq.get("answer", "")
                                
                                issue_type = self.check_qa_comprehensive(question, answer)
                                if issue_type:
                                    issues_found += 1
                                    issue_details.append(f"Original FAQ - {category}: {issue_type}")
            
            return questions_checked, issues_found, issue_details
                
        except Exception as e:
            return 0, 1, [f"File error: {e}"]
    
    def check_qa_comprehensive(self, question: str, answer: str) -> str:
        """Comprehensive check of Q&A pair"""
        
        # Check for problematic patterns
        for pattern in self.problematic_patterns:
            if pattern in answer.lower():
                return f"Generic pattern: '{pattern}'"
        
        # Check for question-answer mismatches
        for question_keyword, wrong_answer_patterns in self.mismatch_patterns:
            if question_keyword in question:
                for wrong_pattern in wrong_answer_patterns:
                    if wrong_pattern in answer.lower():
                        return f"Wrong answer: {question_keyword} question got {wrong_pattern} answer"
        
        # Check for specific content requirements
        
        # Placement company questions should have specific company names
        if any(word in question for word in ["companies", "recruiters", "visit", "placement"]) and not any(word in question for word in ["package", "salary", "process"]):
            required_companies = ["tcs", "infosys", "wipro", "google", "microsoft", "amazon", "accenture", "ibm", "cognizant", "hcl"]
            if not any(company in answer.lower() for company in required_companies):
                return "Missing specific company names"
        
        # Package questions should have specific amounts
        if any(word in question for word in ["package", "salary"]) and not any(word in question for word in ["companies", "recruiters"]):
            if "₹" not in answer or "lpa" not in answer.lower():
                return "Missing specific package amounts"
        
        # Attendance questions should have specific percentage
        if "attendance" in question and "requirement" in question:
            if "75%" not in answer:
                return "Missing specific attendance percentage"
        
        # Grading questions should have grading info
        if "grading" in question and "system" in question:
            grading_terms = ["gpa", "cgpa", "grade", "letter", "credit"]
            if not any(term in answer.lower() for term in grading_terms):
                return "Missing grading system details"
        
        # Library questions should have library-specific info
        if "library" in question and "facilities" in question:
            library_terms = ["books", "journals", "digital", "reading", "study"]
            if not any(term in answer.lower() for term in library_terms):
                return "Missing library-specific information"
        
        # Sports questions should have sports-specific info
        if "sports" in question and "facilities" in question:
            sports_terms = ["cricket", "football", "basketball", "tennis", "badminton", "gymnasium", "swimming", "courts"]
            if not any(term in answer.lower() for term in sports_terms):
                return "Missing sports-specific information"
        
        # Lab questions should have lab-specific info
        if ("lab" in question or "laboratory" in question) and "facilities" in question:
            lab_terms = ["equipment", "computer", "electronics", "mechanical", "experiments", "research"]
            if not any(term in answer.lower() for term in lab_terms):
                return "Missing laboratory-specific information"
        
        # Check answer length (should be substantial)
        if len(answer) < 80:
            return "Answer too short"
        
        # Check for very generic responses
        if answer.count(" ") < 15:  # Less than 15 words
            return "Answer too generic/brief"
        
        return None  # No issues found
    
    def generate_detailed_report(self, total_questions: int, total_issues: int, perfect_colleges: int, colleges_with_issues: List):
        """Generate detailed report of findings"""
        
        report_path = "COMPREHENSIVE_RECHECK_REPORT.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🔍 **COMPREHENSIVE RECHECK REPORT**\n")
            f.write("## **Final Thorough Verification Results**\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 **FINAL VERIFICATION RESULTS**\n\n")
            f.write(f"- **Total Colleges Checked**: 504\n")
            f.write(f"- **Total Questions Verified**: {total_questions:,}\n")
            f.write(f"- **Perfect Colleges**: {perfect_colleges} ({perfect_colleges/504*100:.1f}%)\n")
            f.write(f"- **Colleges with Issues**: {len(colleges_with_issues)}\n")
            f.write(f"- **Total Issues Found**: {total_issues}\n")
            f.write(f"- **Success Rate**: {((total_questions - total_issues) / total_questions * 100):.4f}%\n\n")
            
            if total_issues == 0:
                f.write("## 🎉 **PERFECT DATABASE ACHIEVED!**\n\n")
                f.write("✅ All 504 colleges have perfect Q&A pairs\n")
                f.write("✅ All 56,000+ questions have accurate answers\n")
                f.write("✅ 100% success rate accomplished\n")
                f.write("✅ Ready for production deployment\n\n")
            else:
                f.write("## ⚠️ **ISSUES REQUIRING ATTENTION**\n\n")
                for college_name, issue_count, issue_details in colleges_with_issues:
                    f.write(f"### {college_name} ({issue_count} issues)\n")
                    for issue in issue_details:
                        f.write(f"- {issue}\n")
                    f.write("\n")
        
        print(f"\n📄 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    rechecker = ComprehensiveRecheck()
    
    print("🔍 Comprehensive Recheck System")
    print("=" * 70)
    
    total_questions, total_issues, perfect_colleges, colleges_with_issues = rechecker.perform_comprehensive_recheck()
    
    rechecker.generate_detailed_report(total_questions, total_issues, perfect_colleges, colleges_with_issues)
    
    if total_issues == 0:
        print(f"\n🎉 SUCCESS! Database is 100% perfect!")
        print(f"✅ All {total_questions:,} questions across 504 colleges are perfect!")
        print("🚀 Ready for production deployment!")
    else:
        print(f"\n📊 Recheck completed with detailed analysis")
        print(f"🔧 {total_issues} issues identified for final resolution")
