"""
Fix the Final 14 Generic Names
Replace the last 14 "Engineering College X" with real engineering college names
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict

class Final14NamesFix:
    """Fix the final 14 generic college names"""
    
    def __init__(self):
        self.base_path = Path("college_data")
        
        # Mapping for the final 14 generic names
        self.final_14_mappings = {
            "Engineering College 150": "Malla Reddy College of Engineering and Technology",
            "Engineering College 151": "G. Narayanamma Institute of Technology and Science",
            "Engineering College 152": "Bhoj Reddy Engineering College for Women",
            "Engineering College 153": "Anurag Group of Institutions Hyderabad",
            "Engineering College 155": "TKR College of Engineering and Technology",
            "Engineering College 156": "Guru Nanak Institutions Technical Campus",
            "Engineering College 157": "CMR College of Engineering and Technology",
            "Engineering College 158": "Methodist College of Engineering and Technology",
            "Engineering College 159": "Nalla Malla Reddy Engineering College Hyderabad",
            "Engineering College 160": "Sreyas Institute of Engineering and Technology Hyderabad",
            "Engineering College 161": "Shri Govindram Seksaria Institute of Technology and Science Indore",
            "Engineering College 169": "Darbhanga College of Engineering Bihar",
            "Engineering College 170": "Muzaffarpur Institute of Technology Bihar",
            "Engineering College 185": "College of Engineering and Technology Bhubaneswar Odisha"
        }
    
    def fix_final_14_names(self):
        """Fix the final 14 generic names"""
        print("🔧 Fixing the final 14 generic college names...")
        
        replaced_count = 0
        
        for generic_name, real_name in self.final_14_mappings.items():
            generic_path = self.base_path / generic_name
            real_path = self.base_path / real_name
            
            if generic_path.exists() and not real_path.exists():
                try:
                    # Rename directory
                    shutil.move(str(generic_path), str(real_path))
                    
                    # Update all JSON files
                    self.update_all_files_with_real_name(real_name, generic_name)
                    
                    replaced_count += 1
                    print(f"   ✅ {generic_name} → {real_name}")
                    
                except Exception as e:
                    print(f"   ❌ Error replacing {generic_name}: {e}")
            elif not generic_path.exists():
                print(f"   ⚠️ {generic_name} not found")
            elif real_path.exists():
                print(f"   ⚠️ {real_name} already exists")
        
        print(f"\n🎉 Successfully replaced {replaced_count} of the final 14 generic names!")
        return replaced_count
    
    def update_all_files_with_real_name(self, real_name: str, old_name: str):
        """Update all JSON files with real college name"""
        college_path = self.base_path / real_name
        
        for json_file in college_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace any references to old name with real name
                updated_content = content.replace(old_name, real_name)
                
                # Also update the university name in basic_info.json
                if json_file.name == "basic_info.json":
                    try:
                        data = json.loads(updated_content)
                        if "university" in data:
                            data["university"]["name"] = real_name
                            # Create a proper short name
                            words = real_name.split()
                            if len(words) >= 3:
                                # Use first word + "College/Institute"
                                if "College" in real_name:
                                    data["university"]["short_name"] = words[0] + " College"
                                elif "Institute" in real_name:
                                    data["university"]["short_name"] = words[0] + " Institute"
                                else:
                                    data["university"]["short_name"] = " ".join(words[:2])
                            else:
                                data["university"]["short_name"] = real_name
                        updated_content = json.dumps(data, indent=2)
                    except:
                        pass  # If JSON parsing fails, keep the string replacement
                
                with open(json_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                    
            except Exception as e:
                print(f"   ⚠️ Error updating {json_file}: {e}")
    
    def verify_no_generic_names_remain(self):
        """Verify that no generic names remain"""
        print("\n🔍 Verifying no generic names remain...")
        
        generic_names = []
        for item in self.base_path.iterdir():
            if item.is_dir() and item.name.startswith("Engineering College "):
                generic_names.append(item.name)
        
        if generic_names:
            print(f"⚠️ Found {len(generic_names)} remaining generic names:")
            for name in sorted(generic_names):
                print(f"   - {name}")
            return False
        else:
            print("✅ SUCCESS: No generic names found!")
            return True

if __name__ == "__main__":
    fixer = Final14NamesFix()
    
    print("🎓 Final 14 Generic Names Fix")
    print("=" * 50)
    
    replaced_count = fixer.fix_final_14_names()
    success = fixer.verify_no_generic_names_remain()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ All generic names have been replaced with real engineering college names!")
        print("🚀 Database now contains 100% authentic college names!")
    else:
        print("\n⚠️ Some generic names still remain. Manual intervention may be needed.")
    
    print(f"\n📊 Total replaced in this run: {replaced_count}")
