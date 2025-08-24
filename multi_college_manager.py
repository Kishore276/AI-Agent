"""
Multi-College Database Manager
Manages data for top 300 engineering colleges in India
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd


class MultiCollegeManager:
    """Manage multiple college databases"""
    
    def __init__(self, base_directory: str = "college_data"):
        self.base_directory = Path(base_directory)
        self.colleges = {}
        self.college_rankings = {}
        
    def discover_colleges(self) -> List[str]:
        """Discover all college directories"""
        if not self.base_directory.exists():
            return []
        
        colleges = []
        for item in self.base_directory.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                colleges.append(item.name)
        
        return sorted(colleges)
    
    def load_college_data(self, college_name: str) -> Dict[str, Any]:
        """Load all data for a specific college"""
        college_path = self.base_directory / college_name
        
        if not college_path.exists():
            raise FileNotFoundError(f"College directory {college_name} not found")
        
        college_data = {}
        json_files = list(college_path.glob("*.json"))
        
        for json_file in json_files:
            file_key = json_file.stem
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    college_data[file_key] = json.load(f)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        return college_data
    
    def load_all_colleges(self) -> Dict[str, Dict[str, Any]]:
        """Load data for all colleges"""
        colleges = self.discover_colleges()
        
        for college in colleges:
            try:
                self.colleges[college] = self.load_college_data(college)
                print(f"✅ Loaded: {college}")
            except Exception as e:
                print(f"❌ Error loading {college}: {e}")
        
        return self.colleges
    
    def get_college_summary(self, college_name: str) -> Dict[str, Any]:
        """Get summary information for a college"""
        if college_name not in self.colleges:
            self.colleges[college_name] = self.load_college_data(college_name)
        
        college_data = self.colleges[college_name]
        basic_info = college_data.get('basic_info', {}).get('university', {})
        
        summary = {
            "name": basic_info.get('name', college_name),
            "short_name": basic_info.get('short_name', ''),
            "type": basic_info.get('type', ''),
            "location": basic_info.get('location', {}),
            "established": basic_info.get('established', ''),
            "nirf_ranking": basic_info.get('accreditation', {}).get('nirf_ranking', {}),
            "student_strength": basic_info.get('student_strength', {}),
            "data_files": list(college_data.keys())
        }
        
        return summary
    
    def search_colleges(self, 
                       state: Optional[str] = None,
                       college_type: Optional[str] = None,
                       ranking_range: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Search colleges based on criteria"""
        
        if not self.colleges:
            self.load_all_colleges()
        
        results = []
        
        for college_name, college_data in self.colleges.items():
            basic_info = college_data.get('basic_info', {}).get('university', {})
            
            # Filter by state
            if state and basic_info.get('location', {}).get('state', '').lower() != state.lower():
                continue
            
            # Filter by type
            if college_type and college_type.lower() not in basic_info.get('type', '').lower():
                continue
            
            # Filter by ranking
            if ranking_range:
                nirf_overall = basic_info.get('accreditation', {}).get('nirf_ranking', {}).get('overall', 999)
                if not (ranking_range[0] <= nirf_overall <= ranking_range[1]):
                    continue
            
            results.append(self.get_college_summary(college_name))
        
        return results
    
    def create_college_comparison(self, college_names: List[str]) -> pd.DataFrame:
        """Create comparison table for multiple colleges"""
        
        comparison_data = []
        
        for college_name in college_names:
            if college_name not in self.colleges:
                try:
                    self.colleges[college_name] = self.load_college_data(college_name)
                except:
                    continue
            
            summary = self.get_college_summary(college_name)
            basic_info = self.colleges[college_name].get('basic_info', {}).get('university', {})
            
            row = {
                'College': summary['name'],
                'Type': summary['type'],
                'State': summary['location'].get('state', ''),
                'Established': summary['established'],
                'NIRF Overall': summary['nirf_ranking'].get('overall', 'N/A'),
                'NIRF Engineering': summary['nirf_ranking'].get('engineering', 'N/A'),
                'Total Students': summary['student_strength'].get('total_students', 'N/A'),
                'Faculty': basic_info.get('faculty', {}).get('total_faculty', 'N/A')
            }
            
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def generate_college_text(self, college_name: str) -> str:
        """Generate formatted text for a college (for RAG system)"""
        
        if college_name not in self.colleges:
            self.colleges[college_name] = self.load_college_data(college_name)
        
        college_data = self.colleges[college_name]
        
        def format_json_to_text(obj, level=0):
            lines = []
            indent = "  " * level
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    formatted_key = key.replace('_', ' ').title()
                    if isinstance(value, (dict, list)):
                        lines.append(f"{indent}**{formatted_key}:**")
                        lines.extend(format_json_to_text(value, level + 1))
                    else:
                        lines.append(f"{indent}**{formatted_key}:** {value}")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, (dict, list)):
                        lines.extend(format_json_to_text(item, level))
                    else:
                        lines.append(f"{indent}- {item}")
            return lines
        
        content_lines = [f"# {college_name} Information\n"]
        
        for file_key, data in college_data.items():
            section_title = file_key.replace('_', ' ').title()
            content_lines.append(f"\n## {section_title}\n")
            content_lines.extend(format_json_to_text(data))
        
        return "\n".join(content_lines)
    
    def create_unified_dataset(self, output_file: str = "all_colleges_data.txt"):
        """Create unified text file for all colleges"""
        
        if not self.colleges:
            self.load_all_colleges()
        
        all_content = []
        
        for college_name in sorted(self.colleges.keys()):
            college_text = self.generate_college_text(college_name)
            all_content.append(college_text)
            all_content.append("\n" + "="*80 + "\n")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(all_content))
        
        print(f"✅ Created unified dataset: {output_file}")
        return output_file


# Top 300 Engineering Colleges Template
TOP_300_COLLEGES = {
    "IITs": [
        "IIT Bombay", "IIT Delhi", "IIT Madras", "IIT Kanpur", "IIT Kharagpur",
        "IIT Roorkee", "IIT Guwahati", "IIT Hyderabad", "IIT Indore", "IIT BHU",
        "IIT Gandhinagar", "IIT Ropar", "IIT Patna", "IIT Mandi", "IIT Jodhpur",
        "IIT Bhubaneswar", "IIT Tirupati", "IIT Palakkad", "IIT Jammu", "IIT Goa",
        "IIT Bhilai", "IIT Dharwad", "IIT Dhanbad"
    ],
    "NITs": [
        "NIT Trichy", "NIT Surathkal", "NIT Warangal", "NIT Calicut", "NIT Rourkela",
        "NIT Kurukshetra", "NIT Jaipur", "NIT Allahabad", "NIT Bhopal", "NIT Nagpur",
        "NIT Durgapur", "NIT Jamshedpur", "NIT Hamirpur", "NIT Jalandhar", "NIT Patna",
        "NIT Raipur", "NIT Agartala", "NIT Arunachal Pradesh", "NIT Delhi", "NIT Goa",
        "NIT Manipur", "NIT Meghalaya", "NIT Mizoram", "NIT Nagaland", "NIT Puducherry",
        "NIT Sikkim", "NIT Srinagar", "NIT Tadepalligudem", "NIT Uttarakhand", "NIT Andhra Pradesh"
    ],
    "IIITs": [
        "IIIT Hyderabad", "IIIT Bangalore", "IIIT Delhi", "IIIT Allahabad", "IIIT Gwalior",
        "IIIT Jabalpur", "IIIT Kancheepuram", "IIIT Lucknow", "IIIT Vadodara", "IIIT Nagpur"
    ],
    "Private_Deemed": [
        "BITS Pilani", "VIT Vellore", "SRM Chennai", "Manipal Institute of Technology",
        "Thapar University", "LPU Punjab", "Amity University", "Lovely Professional University"
    ],
    "State_Government": [
        "Anna University", "Jadavpur University", "Delhi Technological University",
        "PSG College of Technology", "Government College of Technology Coimbatore"
    ]
}


def create_college_template(college_name: str, college_info: Dict[str, Any]) -> None:
    """Create basic template files for a college"""

    college_path = Path("college_data") / college_name
    college_path.mkdir(parents=True, exist_ok=True)

    # Basic info template
    basic_info = {
        "university": {
            "name": college_info.get("name", college_name),
            "short_name": college_info.get("short_name", ""),
            "established": college_info.get("established", ""),
            "type": college_info.get("type", ""),
            "location": college_info.get("location", {}),
            "contact": college_info.get("contact", {}),
            "accreditation": college_info.get("accreditation", {}),
            "campus": college_info.get("campus", {}),
            "facilities": college_info.get("facilities", []),
            "student_strength": college_info.get("student_strength", {}),
            "faculty": college_info.get("faculty", {})
        }
    }

    with open(college_path / "basic_info.json", 'w', encoding='utf-8') as f:
        json.dump(basic_info, f, indent=2)

    print(f"✅ Created template for {college_name}")


if __name__ == "__main__":
    print("🎓 Multi-College Database Manager")
    print("=" * 50)

    manager = MultiCollegeManager()

    # Discover existing colleges
    colleges = manager.discover_colleges()
    print(f"Found {len(colleges)} colleges:")
    for college in colleges:
        print(f"  - {college}")

    # Load all data
    if colleges:
        print("\n📚 Loading college data...")
        manager.load_all_colleges()

        # Create comparison
        if len(colleges) > 1:
            print("\n📊 Creating comparison...")
            comparison = manager.create_college_comparison(colleges[:5])  # First 5 colleges
            print(comparison.to_string(index=False))

        # Create unified dataset
        print("\n📝 Creating unified dataset...")
        manager.create_unified_dataset()

    print(f"\n✅ Management complete!")
    print(f"Total colleges in database: {len(colleges)}")
    print(f"Target: 300 engineering colleges")
    print(f"Remaining: {300 - len(colleges)}")
