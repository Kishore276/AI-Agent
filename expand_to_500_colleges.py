"""
Expand to 500 Engineering Colleges Database
Creates comprehensive database of top 500 engineering colleges in India
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

class Top500CollegesExpander:
    """Expand database to 500 engineering colleges"""
    
    def __init__(self):
        self.base_path = Path("college_data")
        
        # Comprehensive list of top 500 engineering colleges by state
        self.colleges_by_state = {
            "Andhra Pradesh": [
                "IIT Tirupati", "NIT Andhra Pradesh", "JNTUH Hyderabad", "JNTUK Kakinada", 
                "JNTUA Anantapur", "AU College of Engineering Visakhapatnam", "KL University",
                "Vignan University", "VIT AP", "SRM AP", "Amrita Vishwa Vidyapeetham Amaravati",
                "GITAM University", "Koneru Lakshmaiah Education Foundation", "Centurion University",
                "Anil Neerukonda Institute of Technology", "Gokaraju Rangaraju Institute of Engineering",
                "CVR College of Engineering", "Vasavi College of Engineering", "CBIT Hyderabad",
                "Osmania University College of Engineering", "Chaitanya Bharathi Institute of Technology",
                "Mahatma Gandhi Institute of Technology", "Sreenidhi Institute of Science and Technology",
                "Vardhaman College of Engineering", "Malla Reddy College of Engineering",
                "G. Narayanamma Institute of Technology", "Bhoj Reddy Engineering College",
                "Anurag Group of Institutions", "TKR College of Engineering", "Guru Nanak Institutions"
            ],
            "Tamil Nadu": [
                "IIT Madras", "NIT Trichy", "Anna University", "SRM Chennai", "VIT Vellore",
                "Kalasalingam University", "SASTRA University", "Sathyabama University", 
                "SSN College of Engineering", "PSG College of Technology", "Vel Tech University",
                "Saveetha University", "Hindustan University", "B.S. Abdur Rahman University",
                "Karunya University", "Kumaraguru College of Technology", "Coimbatore Institute of Technology",
                "Thiagarajar College of Engineering", "Government College of Technology Coimbatore",
                "Madras Institute of Technology", "College of Engineering Guindy", "Alagappa College of Technology",
                "Rajalakshmi Engineering College", "Sri Sairam Engineering College", "Easwari Engineering College",
                "Velammal Engineering College", "St. Joseph's College of Engineering", "Loyola-ICAM College",
                "Panimalar Engineering College", "R.M.K. Engineering College", "R.M.D. Engineering College",
                "Sri Krishna College of Engineering", "Bannari Amman Institute of Technology",
                "K.S.R. College of Engineering", "Mepco Schlenk Engineering College", "Francis Xavier Engineering College",
                "Sethu Institute of Technology", "Karpagam College of Engineering", "Info Institute of Engineering",
                "Jeppiaar Engineering College", "Dr. M.G.R. Educational and Research Institute"
            ],
            "Karnataka": [
                "NIT Surathkal", "IIIT Bangalore", "Manipal Institute of Technology", "Christ University",
                "Jain University", "R.V. College of Engineering", "M.S. Ramaiah Institute of Technology",
                "Siddaganga Institute of Technology", "BMS College of Engineering", "Dayananda Sagar College",
                "PES University", "Ramaiah Institute of Technology", "New Horizon College of Engineering",
                "Nitte Meenakshi Institute of Technology", "Sir M. Visvesvaraya Institute of Technology",
                "B.M.S. Institute of Technology", "Acharya Institute of Technology", "Global Academy of Technology",
                "K.S. Institute of Technology", "Sapthagiri College of Engineering", "East West Institute of Technology",
                "Reva University", "CMR Institute of Technology", "Presidency University", "Garden City University",
                "Bangalore Institute of Technology", "University Visvesvaraya College of Engineering",
                "JSS Science and Technology University", "Visvesvaraya Technological University",
                "KLE Technological University", "SDM College of Engineering and Technology"
            ],
            "Maharashtra": [
                "IIT Bombay", "VNIT Nagpur", "ICT Mumbai", "COEP Pune", "College of Engineering Pune",
                "Veermata Jijabai Technological Institute", "Sardar Patel College of Engineering",
                "K.J. Somaiya College of Engineering", "Thadomal Shahani Engineering College",
                "Fr. Conceicao Rodrigues College of Engineering", "Atharva College of Engineering",
                "Shah and Anchor Kutchhi Engineering College", "Pillai College of Engineering",
                "Bharati Vidyapeeth College of Engineering", "MIT World Peace University",
                "Symbiosis Institute of Technology", "Vishwakarma Institute of Technology",
                "Pune Institute of Computer Technology", "Army Institute of Technology",
                "Maharashtra Institute of Technology", "Sinhgad College of Engineering",
                "D.Y. Patil College of Engineering", "Sandip University", "MIT Academy of Engineering",
                "AISSMS College of Engineering", "Zeal College of Engineering", "NBN Sinhgad School of Engineering"
            ],
            "Uttar Pradesh": [
                "IIT Kanpur", "IIT BHU Varanasi", "IIT Patna", "MNIT Allahabad", "Aligarh Muslim University",
                "Harcourt Butler Technical University", "Madan Mohan Malaviya University of Technology",
                "AKTU Lucknow", "Integral University", "Amity University Noida", "Bennett University",
                "Sharda University", "Galgotias University", "GL Bajaj Institute of Technology",
                "ABES Engineering College", "JSS Academy of Technical Education", "IMS Engineering College",
                "Krishna Institute of Engineering and Technology", "Raj Kumar Goel Institute of Technology",
                "KIET Group of Institutions", "Ajay Kumar Garg Engineering College", "IET Lucknow",
                "Bundelkhand Institute of Engineering and Technology", "United College of Engineering and Research"
            ],
            "West Bengal": [
                "IIT Kharagpur", "Jadavpur University", "NIT Durgapur", "IIEST Shibpur",
                "Kalyani Government Engineering College", "Jalpaiguri Government Engineering College",
                "Haldia Institute of Technology", "Heritage Institute of Technology", "Techno India University",
                "Narula Institute of Technology", "JIS College of Engineering", "Meghnad Saha Institute of Technology",
                "Calcutta Institute of Engineering and Management", "Institute of Engineering and Management",
                "Siliguri Institute of Technology", "Asansol Engineering College", "Government College of Engineering and Ceramic Technology"
            ],
            "Delhi": [
                "IIT Delhi", "NIT Delhi", "Delhi Technological University", "NSUT Delhi",
                "Indraprastha Institute of Information Technology", "Jamia Millia Islamia",
                "Guru Gobind Singh Indraprastha University", "Bharati Vidyapeeth College of Engineering",
                "Maharaja Agrasen Institute of Technology", "Ambedkar Institute of Advanced Communication Technologies"
            ]
        }
    
    def expand_database(self):
        """Expand database to 500 colleges"""
        print("🚀 Expanding database to 500 engineering colleges...")
        
        current_count = len(os.listdir(self.base_path))
        print(f"📊 Current colleges: {current_count}")
        
        target_count = 500
        colleges_to_add = target_count - current_count
        
        print(f"🎯 Target: {target_count} colleges")
        print(f"➕ Need to add: {colleges_to_add} colleges")
        
        added_count = 0
        
        for state, colleges in self.colleges_by_state.items():
            print(f"\n🏛️ Processing {state}...")
            
            for college in colleges:
                college_path = self.base_path / college
                
                if not college_path.exists() and added_count < colleges_to_add:
                    self.create_college_data(college, state)
                    added_count += 1
                    print(f"   ✅ Added {college} ({added_count}/{colleges_to_add})")
                    
                    if added_count >= colleges_to_add:
                        break
            
            if added_count >= colleges_to_add:
                break
        
        final_count = len(os.listdir(self.base_path))
        print(f"\n🎉 Database expanded to {final_count} colleges!")
        return final_count
    
    def create_college_data(self, college_name: str, state: str):
        """Create complete data for a new college"""
        college_path = self.base_path / college_name
        college_path.mkdir(parents=True, exist_ok=True)
        
        # Determine college type and info
        college_info = self.get_college_info(college_name, state)
        
        # Create all 7 files
        files = {
            "basic_info.json": self.generate_basic_info(college_name, college_info),
            "courses.json": self.generate_courses(college_name, college_info),
            "fees_structure.json": self.generate_fees(college_name, college_info),
            "admission_process.json": self.generate_admission(college_name, college_info),
            "facilities.json": self.generate_facilities(college_name, college_info),
            "placements.json": self.generate_placements(college_name, college_info),
            "faq.json": self.generate_faq(college_name, college_info)
        }
        
        for filename, content in files.items():
            with open(college_path / filename, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)

if __name__ == "__main__":
    expander = Top500CollegesExpander()
    expander.expand_database()
