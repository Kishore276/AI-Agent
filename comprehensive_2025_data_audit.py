#!/usr/bin/env python3
"""
Comprehensive 2025 Data Audit and Update
Check all college data for accuracy, currency, and consistency as of August 2025
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
import re
from datetime import datetime

class Comprehensive2025DataAudit:
    """Comprehensive audit system for 2025 data standards"""
    
    def __init__(self):
        self.base_path = Path("college_data")
        self.issues_found = []
        self.corrections_made = []
        
        # 2025 Current Data Standards
        self.current_standards_2025 = {
            "academic_year": "2025-2026",
            "current_year": 2025,
            "last_updated_month": "August 2025",
            
            "jee_dates_2025": {
                "jee_main_session1": "January 24 - February 1, 2025",
                "jee_main_session2": "April 1 - April 8, 2025",
                "jee_advanced": "May 18, 2025",
                "jee_advanced_result": "June 9, 2025",
                "josaa_counseling": "June 10 - August 25, 2025",
                "csab_counseling": "August 26 - September 30, 2025",
                "classes_start": "August 2025"
            },
            
            "fee_structures_2025_26": {
                "IIT": {
                    "tuition": 250000,
                    "hostel": 150000,
                    "total_annual": 400000,
                    "description": "₹2,50,000 (Tuition) + ₹1,50,000 (Hostel & Mess)"
                },
                "NIT": {
                    "tuition": 175000,
                    "hostel": 75000,
                    "total_annual": 250000,
                    "description": "₹1,75,000 (Tuition) + ₹75,000 (Hostel & Mess)"
                },
                "IIIT": {
                    "tuition": 200000,
                    "hostel": 100000,
                    "total_annual": 300000,
                    "description": "₹2,00,000 (Tuition) + ₹1,00,000 (Hostel & Mess)"
                },
                "Private_Tier1": {
                    "tuition": 300000,
                    "hostel": 150000,
                    "total_annual": 450000,
                    "description": "₹3,00,000 - ₹4,50,000 per year"
                },
                "Private_Tier2": {
                    "tuition": 200000,
                    "hostel": 100000,
                    "total_annual": 300000,
                    "description": "₹2,00,000 - ₹3,00,000 per year"
                },
                "Government": {
                    "tuition": 100000,
                    "hostel": 50000,
                    "total_annual": 150000,
                    "description": "₹1,00,000 - ₹1,50,000 per year"
                }
            },
            
            "nirf_rankings_2024": {
                "IIT Madras": 1,
                "IIT Delhi": 2,
                "IIT Bombay": 3,
                "IIT Kanpur": 4,
                "IIT Kharagpur": 5,
                "IIT Roorkee": 6,
                "IIT Guwahati": 7,
                "IIT Hyderabad": 8,
                "IISC Bangalore": 9,
                "IIT Indore": 10,
                "NIT Trichy": 11,
                "NIT Surathkal": 12,
                "NIT Warangal": 13,
                "IIT BHU": 14,
                "IIT Ropar": 15,
                "IIIT Hyderabad": 16,
                "NIT Calicut": 17,
                "DTU Delhi": 18,
                "IIT Gandhinagar": 19,
                "IIT Patna": 20
            },
            
            "placement_data_2024_25": {
                "IIT": {
                    "average_package": "18-25 LPA",
                    "highest_package": "80-150 LPA",
                    "placement_percentage": "95-98%",
                    "top_recruiters": ["Google", "Microsoft", "Amazon", "Goldman Sachs", "McKinsey"]
                },
                "NIT": {
                    "average_package": "12-18 LPA",
                    "highest_package": "40-80 LPA", 
                    "placement_percentage": "85-95%",
                    "top_recruiters": ["TCS", "Infosys", "Wipro", "Accenture", "IBM"]
                },
                "IIIT": {
                    "average_package": "15-20 LPA",
                    "highest_package": "50-100 LPA",
                    "placement_percentage": "90-95%",
                    "top_recruiters": ["Adobe", "Samsung", "Qualcomm", "Intel", "Nvidia"]
                }
            },
            
            "entrance_exams_2025": {
                "IIT": ["JEE Advanced 2025"],
                "NIT": ["JEE Main 2025"],
                "IIIT": ["JEE Main 2025"],
                "Private": ["JEE Main 2025", "State CET 2025"],
                "Government": ["JEE Main 2025", "State CET 2025"]
            }
        }
        
        # Common data issues to check for
        self.check_patterns = {
            "outdated_year": ["2024-25", "2023-24", "2022-23", "2024-2025", "2023-2024"],
            "outdated_jee_dates": ["2024", "2023", "January 2024", "April 2024"],
            "generic_names": ["Engineering College", "Institute of Technology", "Technical University"],
            "incorrect_fees": ["₹50,000", "₹1,00,000", "₹5,00,000 per semester"],
            "old_placement_data": ["2023", "2022", "2021"]
        }
    
    def audit_all_colleges(self):
        """Main audit function"""
        print("🔍 COMPREHENSIVE 2025 DATA AUDIT - AUGUST UPDATE")
        print("=" * 70)
        print(f"📅 Current Standards: Academic Year {self.current_standards_2025['academic_year']}")
        print(f"📊 Audit Date: {datetime.now().strftime('%B %d, %Y')}")
        print()
        
        if not self.base_path.exists():
            print("❌ College data directory not found!")
            return
        
        colleges = [d for d in os.listdir(self.base_path) if os.path.isdir(self.base_path / d)]
        total_colleges = len(colleges)
        
        print(f"📚 Found {total_colleges} colleges to audit")
        print()
        
        issues_summary = {
            "outdated_academic_year": 0,
            "incorrect_jee_dates": 0,
            "wrong_fee_structure": 0,
            "outdated_placement_data": 0,
            "missing_nirf_rankings": 0,
            "generic_college_names": 0,
            "incomplete_data_files": 0
        }
        
        colleges_with_issues = []
        perfect_colleges = []
        
        for i, college_name in enumerate(sorted(colleges), 1):
            print(f"🔍 [{i:3d}/{total_colleges}] Auditing: {college_name}")
            
            college_issues = self.audit_single_college(college_name)
            
            if college_issues:
                colleges_with_issues.append((college_name, college_issues))
                for issue_type in college_issues:
                    if issue_type in issues_summary:
                        issues_summary[issue_type] += 1
                print(f"   ⚠️  Found {len(college_issues)} issue(s): {', '.join(college_issues)}")
            else:
                perfect_colleges.append(college_name)
                print(f"   ✅ Perfect - meets all 2025 standards")
        
        # Generate comprehensive audit report
        self.generate_audit_report(total_colleges, colleges_with_issues, perfect_colleges, issues_summary)
        
        return colleges_with_issues, perfect_colleges, issues_summary
    
    def audit_single_college(self, college_name: str) -> List[str]:
        """Audit a single college for all data issues"""
        college_path = self.base_path / college_name
        issues = []
        
        # Required files for each college
        required_files = [
            "basic_info.json",
            "courses.json", 
            "fees_structure.json",
            "admission_process.json",
            "facilities.json",
            "placements.json",
            "faq.json"
        ]
        
        # Check if all required files exist
        for file_name in required_files:
            file_path = college_path / file_name
            if not file_path.exists():
                issues.append("incomplete_data_files")
                continue
            
            # Check content of each file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # File-specific checks
                if file_name == "basic_info.json":
                    issues.extend(self.check_basic_info(data, college_name))
                elif file_name == "fees_structure.json":
                    issues.extend(self.check_fees_structure(data, college_name))
                elif file_name == "admission_process.json":
                    issues.extend(self.check_admission_process(data))
                elif file_name == "placements.json":
                    issues.extend(self.check_placements_data(data))
                
            except (json.JSONDecodeError, Exception):
                issues.append("corrupted_json_file")
        
        return list(set(issues))  # Remove duplicates
    
    def check_basic_info(self, data: Dict, college_name: str) -> List[str]:
        """Check basic info for current standards"""
        issues = []
        
        # Check academic year
        academic_year = data.get("academic_year", "")
        if academic_year != self.current_standards_2025["academic_year"]:
            issues.append("outdated_academic_year")
        
        # Check for generic names
        for generic in self.check_patterns["generic_names"]:
            if generic in college_name and len(college_name.split()) <= 3:
                issues.append("generic_college_names")
                break
        
        # Check NIRF ranking for top institutions
        college_type = self.determine_college_type(college_name)
        if college_type in ["IIT", "NIT", "IIIT"] and "nirf_ranking" not in data:
            issues.append("missing_nirf_rankings")
        
        return issues
    
    def check_fees_structure(self, data: Dict, college_name: str) -> List[str]:
        """Check fee structure for 2025-26 standards"""
        issues = []
        
        college_type = self.determine_college_type(college_name)
        expected_fees = self.current_standards_2025["fee_structures_2025_26"].get(college_type)
        
        if expected_fees:
            total_fees = data.get("total_annual_fees", 0)
            if isinstance(total_fees, str):
                # Extract numeric value from string
                total_fees = int(re.sub(r'[^\d]', '', total_fees)) if re.sub(r'[^\d]', '', total_fees) else 0
            
            expected_range = expected_fees["total_annual"]
            if total_fees < expected_range * 0.7 or total_fees > expected_range * 1.5:
                issues.append("wrong_fee_structure")
        
        # Check for outdated academic year in fee structure
        fee_text = str(data)
        for outdated_year in self.check_patterns["outdated_year"]:
            if outdated_year in fee_text:
                issues.append("outdated_academic_year")
                break
        
        return issues
    
    def check_admission_process(self, data: Dict) -> List[str]:
        """Check admission process for 2025 dates"""
        issues = []
        
        admission_text = str(data)
        
        # Check for outdated JEE dates
        for outdated_date in self.check_patterns["outdated_jee_dates"]:
            if outdated_date in admission_text:
                issues.append("incorrect_jee_dates")
                break
        
        return issues
    
    def check_placements_data(self, data: Dict) -> List[str]:
        """Check placement data for currency"""
        issues = []
        
        placement_text = str(data)
        
        # Check for old placement years
        for old_year in self.check_patterns["old_placement_data"]:
            if old_year in placement_text:
                issues.append("outdated_placement_data")
                break
        
        return issues
    
    def determine_college_type(self, college_name: str) -> str:
        """Determine college type from name"""
        college_name_upper = college_name.upper()
        
        if "IIT" in college_name_upper:
            return "IIT"
        elif "NIT" in college_name_upper:
            return "NIT"
        elif "IIIT" in college_name_upper:
            return "IIIT"
        elif any(word in college_name_upper for word in ["GOVERNMENT", "GOVT"]):
            return "Government"
        else:
            # Determine if it's tier 1 or tier 2 private college
            tier1_indicators = ["BITS", "VIT", "SRM", "MANIPAL", "AMITY", "LPU"]
            if any(indicator in college_name_upper for indicator in tier1_indicators):
                return "Private_Tier1"
            else:
                return "Private_Tier2"
    
    def generate_audit_report(self, total_colleges: int, colleges_with_issues: List, 
                            perfect_colleges: List, issues_summary: Dict):
        """Generate comprehensive audit report"""
        print("\n" + "="*70)
        print("📊 COMPREHENSIVE 2025 DATA AUDIT REPORT")
        print("="*70)
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   📚 Total Colleges Audited: {total_colleges}")
        print(f"   ✅ Perfect Colleges: {len(perfect_colleges)} ({len(perfect_colleges)/total_colleges*100:.1f}%)")
        print(f"   ⚠️  Colleges with Issues: {len(colleges_with_issues)} ({len(colleges_with_issues)/total_colleges*100:.1f}%)")
        
        print(f"\n🔍 ISSUES BREAKDOWN:")
        for issue_type, count in issues_summary.items():
            if count > 0:
                print(f"   • {issue_type.replace('_', ' ').title()}: {count} colleges")
        
        print(f"\n⚠️  COLLEGES REQUIRING UPDATES:")
        if colleges_with_issues:
            for college_name, issues in colleges_with_issues[:20]:  # Show first 20
                print(f"   📝 {college_name}: {', '.join(issues)}")
            if len(colleges_with_issues) > 20:
                print(f"   ... and {len(colleges_with_issues) - 20} more colleges")
        else:
            print("   🎉 All colleges meet 2025 standards!")
        
        # Save detailed report to file
        report_file = "COMPREHENSIVE_2025_AUDIT_REPORT.md"
        self.save_detailed_report(report_file, total_colleges, colleges_with_issues, 
                                perfect_colleges, issues_summary)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        print(f"✅ Audit completed successfully!")
    
    def save_detailed_report(self, filename: str, total_colleges: int, 
                           colleges_with_issues: List, perfect_colleges: List, 
                           issues_summary: Dict):
        """Save detailed audit report to markdown file"""
        report_content = f"""# 🔍 COMPREHENSIVE 2025 DATA AUDIT REPORT
## Engineering Colleges Data Verification - August 2025

---

## 📊 **AUDIT SUMMARY**

### **Overall Results:**
- **Total Colleges Audited**: {total_colleges}
- **Perfect Colleges**: {len(perfect_colleges)} ({len(perfect_colleges)/total_colleges*100:.1f}%)
- **Colleges Requiring Updates**: {len(colleges_with_issues)} ({len(colleges_with_issues)/total_colleges*100:.1f}%)
- **Audit Date**: {datetime.now().strftime('%B %d, %Y')}

---

## 🎯 **2025 DATA STANDARDS CHECKED**

### **Academic Year**: 2025-2026
### **JEE Dates**: 
- JEE Main Session 1: January 24 - February 1, 2025
- JEE Main Session 2: April 1 - April 8, 2025  
- JEE Advanced: May 18, 2025

### **Fee Structures (2025-26)**:
- **IIT**: ₹4,00,000 per year
- **NIT**: ₹2,50,000 per year
- **IIIT**: ₹3,00,000 per year

---

## 🔍 **ISSUES IDENTIFIED**

"""
        
        for issue_type, count in issues_summary.items():
            if count > 0:
                report_content += f"### **{issue_type.replace('_', ' ').title()}**: {count} colleges\n\n"
        
        report_content += "---\n\n## 📝 **COLLEGES REQUIRING UPDATES**\n\n"
        
        if colleges_with_issues:
            for college_name, issues in colleges_with_issues:
                report_content += f"### {college_name}\n"
                report_content += f"**Issues**: {', '.join(issues)}\n\n"
        else:
            report_content += "🎉 **All colleges meet 2025 standards!**\n\n"
        
        report_content += "---\n\n## ✅ **PERFECT COLLEGES**\n\n"
        
        if perfect_colleges:
            for i, college in enumerate(perfect_colleges, 1):
                if i % 10 == 1:
                    report_content += f"**Colleges {i}-{min(i+9, len(perfect_colleges))}:**\n"
                report_content += f"{i}. {college}\n"
                if i % 10 == 0:
                    report_content += "\n"
        
        report_content += f"""

---

## 📈 **RECOMMENDATIONS**

1. **Update Academic Years**: Change all instances of old academic years to 2025-2026
2. **Update JEE Dates**: Replace all 2024 JEE dates with 2025 dates
3. **Verify Fee Structures**: Ensure all fees reflect 2025-26 academic year rates
4. **Update Placement Data**: Include latest 2024-25 placement statistics
5. **Add NIRF Rankings**: Include 2024 NIRF rankings for eligible institutions

---

**Generated on**: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)

def main():
    """Main execution function"""
    auditor = Comprehensive2025DataAudit()
    colleges_with_issues, perfect_colleges, issues_summary = auditor.audit_all_colleges()
    
    # If issues found, offer to auto-fix them
    if colleges_with_issues:
        print(f"\n🔧 Found {len(colleges_with_issues)} colleges with data issues.")
        print("Would you like to auto-fix these issues? (This will update the data files)")
        
        # For now, just report. Auto-fix can be implemented separately
        print("💡 Review the audit report and manually update the identified issues.")
    
    return colleges_with_issues, perfect_colleges

if __name__ == "__main__":
    main()
