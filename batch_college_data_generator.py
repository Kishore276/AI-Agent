"""
Batch College Data Generator
Creates all 7 JSON files for all colleges in the database
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

class BatchCollegeDataGenerator:
    """Generate comprehensive data for all colleges"""
    
    def __init__(self):
        self.base_path = Path("college_data")
        self.required_files = [
            "basic_info.json",
            "courses.json", 
            "fees_structure.json",
            "admission_process.json",
            "facilities.json",
            "placements.json",
            "faq.json"
        ]
        
    def get_existing_colleges(self) -> List[str]:
        """Get list of existing college directories"""
        if not self.base_path.exists():
            return []
        
        colleges = []
        for item in self.base_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                colleges.append(item.name)
        
        return sorted(colleges)
    
    def check_missing_files(self, college_name: str) -> List[str]:
        """Check which files are missing for a college"""
        college_path = self.base_path / college_name
        if not college_path.exists():
            return self.required_files
        
        missing_files = []
        for file_name in self.required_files:
            if not (college_path / file_name).exists():
                missing_files.append(file_name)
        
        return missing_files
    
    def generate_missing_files(self):
        """Generate all missing files for all colleges"""
        colleges = self.get_existing_colleges()
        
        print(f"🎓 Found {len(colleges)} colleges")
        print("📋 Checking for missing files...")
        
        total_files_created = 0
        
        for college in colleges:
            missing_files = self.check_missing_files(college)
            if missing_files:
                print(f"\n🏫 {college}:")
                print(f"   Missing files: {', '.join(missing_files)}")
                
                for file_name in missing_files:
                    self.create_file_for_college(college, file_name)
                    total_files_created += 1
            else:
                print(f"✅ {college}: All files present")
        
        print(f"\n🎉 Created {total_files_created} files across all colleges")
        return total_files_created
    
    def create_file_for_college(self, college_name: str, file_name: str):
        """Create a specific file for a college"""
        college_path = self.base_path / college_name
        college_path.mkdir(parents=True, exist_ok=True)
        
        file_path = college_path / file_name
        
        # Generate content based on file type
        if file_name == "courses.json":
            content = self.generate_courses_template(college_name)
        elif file_name == "admission_process.json":
            content = self.generate_admission_template(college_name)
        elif file_name == "facilities.json":
            content = self.generate_facilities_template(college_name)
        elif file_name == "placements.json":
            content = self.generate_placements_template(college_name)
        elif file_name == "faq.json":
            content = self.generate_faq_template(college_name)
        elif file_name == "fees_structure.json":
            content = self.generate_fees_template(college_name)
        else:
            content = {}
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
        
        print(f"   ✅ Created {file_name}")
    
    def get_college_type(self, college_name: str) -> str:
        """Determine college type"""
        if "IIT" in college_name:
            return "IIT"
        elif "NIT" in college_name:
            return "NIT"
        elif "IIIT" in college_name:
            return "IIIT"
        elif college_name in ["BITS Pilani", "VIT Vellore", "SRM Chennai", "Manipal Institute of Technology", "Thapar University"]:
            return "Private"
        else:
            return "State"
    
    def generate_courses_template(self, college_name: str) -> Dict:
        """Generate courses.json template"""
        college_type = self.get_college_type(college_name)
        
        base_template = {
            "undergraduate_programs": {
                "engineering": {
                    "btech": {
                        "duration": "4 years",
                        "total_semesters": 8,
                        "eligibility": "JEE Advanced qualified" if college_type == "IIT" else "JEE Main qualified",
                        "admission_process": ["JEE Advanced"] if college_type == "IIT" else ["JEE Main", "State CET"],
                        "departments": self.get_departments_by_type(college_type)
                    }
                }
            },
            "postgraduate_programs": {
                "mtech": {
                    "duration": "2 years",
                    "admission": "GATE qualified",
                    "programs": [
                        {"name": "Computer Science and Engineering", "specializations": ["AI & ML", "Systems"], "intake": 50},
                        {"name": "Electrical Engineering", "specializations": ["Power Systems", "VLSI"], "intake": 40},
                        {"name": "Mechanical Engineering", "specializations": ["Thermal", "Design"], "intake": 35}
                    ]
                }
            },
            "doctoral_programs": {
                "phd": {
                    "duration": "4-6 years",
                    "areas": ["Engineering", "Science", "Management"]
                }
            }
        }
        
        return base_template
    
    def get_departments_by_type(self, college_type: str) -> List[Dict]:
        """Get departments based on college type"""
        if college_type == "IIT":
            return [
                {
                    "name": "Computer Science and Engineering",
                    "code": "CSE",
                    "specializations": ["AI", "ML", "Systems", "Theory"],
                    "intake": 120,
                    "faculty_count": 65,
                    "labs": ["AI Lab", "Systems Lab", "Networks Lab"]
                },
                {
                    "name": "Electrical Engineering", 
                    "code": "EE",
                    "specializations": ["Power Systems", "Electronics", "Communication"],
                    "intake": 120,
                    "faculty_count": 70,
                    "labs": ["Power Lab", "Electronics Lab", "Communication Lab"]
                },
                {
                    "name": "Mechanical Engineering",
                    "code": "ME", 
                    "specializations": ["Thermal", "Design", "Manufacturing"],
                    "intake": 120,
                    "faculty_count": 60,
                    "labs": ["Manufacturing Lab", "Thermal Lab", "Materials Lab"]
                }
            ]
        else:
            return [
                {
                    "name": "Computer Science and Engineering",
                    "code": "CSE",
                    "specializations": ["Software Engineering", "Data Science"],
                    "intake": 180,
                    "faculty_count": 45,
                    "labs": ["Programming Lab", "Database Lab"]
                },
                {
                    "name": "Electronics and Communication Engineering",
                    "code": "ECE",
                    "specializations": ["VLSI", "Communication Systems"],
                    "intake": 120,
                    "faculty_count": 35,
                    "labs": ["Electronics Lab", "Communication Lab"]
                }
            ]

if __name__ == "__main__":
    generator = BatchCollegeDataGenerator()
    generator.generate_missing_files()
