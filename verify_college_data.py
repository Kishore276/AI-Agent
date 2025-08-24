"""
Verification Script for College Data Completeness
Checks if all colleges have all 7 required JSON files
"""

import os
from pathlib import Path

def verify_all_colleges():
    """Verify all colleges have complete data"""
    base_path = Path("college_data")
    required_files = [
        "basic_info.json",
        "courses.json", 
        "fees_structure.json",
        "admission_process.json",
        "facilities.json",
        "placements.json",
        "faq.json"
    ]
    
    colleges = []
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            colleges.append(item.name)
    
    colleges.sort()
    
    print("🎓 College Data Verification Report")
    print("=" * 60)
    print(f"📊 Total Colleges: {len(colleges)}")
    print(f"📋 Required Files per College: {len(required_files)}")
    print(f"🎯 Target Total Files: {len(colleges) * len(required_files)}")
    print("\n" + "=" * 60)
    
    complete_colleges = 0
    total_files_found = 0
    
    for college in colleges:
        college_path = base_path / college
        files_present = []
        files_missing = []
        
        for file_name in required_files:
            if (college_path / file_name).exists():
                files_present.append(file_name)
                total_files_found += 1
            else:
                files_missing.append(file_name)
        
        status = "✅ COMPLETE" if len(files_missing) == 0 else f"❌ MISSING {len(files_missing)}"
        print(f"{status} | {college}")
        
        if files_missing:
            print(f"         Missing: {', '.join(files_missing)}")
        else:
            complete_colleges += 1
        
        print(f"         Files: {len(files_present)}/{len(required_files)}")
    
    print("\n" + "=" * 60)
    print("📈 SUMMARY STATISTICS")
    print("=" * 60)
    print(f"✅ Complete Colleges: {complete_colleges}/{len(colleges)} ({complete_colleges/len(colleges)*100:.1f}%)")
    print(f"📁 Total Files Created: {total_files_found}/{len(colleges) * len(required_files)} ({total_files_found/(len(colleges) * len(required_files))*100:.1f}%)")
    print(f"🎯 Files per College: {total_files_found/len(colleges):.1f} average")
    
    if complete_colleges == len(colleges):
        print("\n🎉 SUCCESS: All colleges have complete data!")
        print("🚀 Ready for comprehensive multi-college chatbot!")
    else:
        print(f"\n⚠️  {len(colleges) - complete_colleges} colleges need attention")
    
    return complete_colleges == len(colleges)

if __name__ == "__main__":
    verify_all_colleges()
