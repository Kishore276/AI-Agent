#!/usr/bin/env python3
"""
Fix College Data Structure Issues
Remove extra ai_agent_data.json files and ensure clean structure
"""

import os
import json
from pathlib import Path

def fix_college_data_structure():
    """Remove extra ai_agent_data.json files from college directories"""
    print("🔧 Fixing college data structure...")
    
    college_data_dir = Path("college_data")
    if not college_data_dir.exists():
        print("❌ College data directory not found")
        return
    
    expected_files = [
        'basic_info.json',
        'courses.json', 
        'fees_structure.json',
        'admission_process.json',
        'facilities.json',
        'placements.json',
        'faq.json'
    ]
    
    colleges_fixed = 0
    files_removed = 0
    
    for college_dir in college_data_dir.iterdir():
        if college_dir.is_dir():
            # Check for ai_agent_data.json
            ai_data_file = college_dir / "ai_agent_data.json"
            
            if ai_data_file.exists():
                try:
                    # Remove the extra file
                    ai_data_file.unlink()
                    files_removed += 1
                    colleges_fixed += 1
                    
                    # Verify we now have exactly 7 files
                    json_files = list(college_dir.glob("*.json"))
                    if len(json_files) == 7:
                        # Check all expected files exist
                        file_names = [f.name for f in json_files]
                        missing = [f for f in expected_files if f not in file_names]
                        if missing:
                            print(f"⚠️ {college_dir.name}: Missing files - {missing}")
                    else:
                        print(f"⚠️ {college_dir.name}: Still has {len(json_files)} files")
                        
                except Exception as e:
                    print(f"❌ Error fixing {college_dir.name}: {e}")
    
    print(f"✅ Fixed {colleges_fixed} colleges")
    print(f"🗑️ Removed {files_removed} extra ai_agent_data.json files")
    
    # Verify the fix
    print("\n🔍 Verifying fix...")
    issues_remaining = 0
    
    for college_dir in college_data_dir.iterdir():
        if college_dir.is_dir():
            json_files = list(college_dir.glob("*.json"))
            if len(json_files) != 7:
                issues_remaining += 1
                print(f"⚠️ {college_dir.name}: {len(json_files)} files")
                
            # Check for any remaining ai_agent_data.json
            if (college_dir / "ai_agent_data.json").exists():
                print(f"⚠️ {college_dir.name}: ai_agent_data.json still exists")
    
    if issues_remaining == 0:
        print("✅ All college directories now have exactly 7 JSON files")
    else:
        print(f"⚠️ {issues_remaining} colleges still have issues")

def verify_json_integrity():
    """Verify all JSON files can be loaded properly"""
    print("\n🔍 Verifying JSON file integrity...")
    
    college_data_dir = Path("college_data")
    corrupted_files = []
    total_files = 0
    
    for college_dir in college_data_dir.iterdir():
        if college_dir.is_dir():
            for json_file in college_dir.glob("*.json"):
                total_files += 1
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        json.load(f)
                except Exception as e:
                    corrupted_files.append(f"{college_dir.name}/{json_file.name}: {e}")
    
    if corrupted_files:
        print(f"❌ Found {len(corrupted_files)} corrupted JSON files:")
        for error in corrupted_files:
            print(f"   - {error}")
    else:
        print(f"✅ All {total_files} JSON files are valid")

if __name__ == "__main__":
    fix_college_data_structure()
    verify_json_integrity()
    print("\n🎉 College data structure fix completed!")
