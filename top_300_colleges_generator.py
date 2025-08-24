"""
Top 300 Engineering Colleges Generator
Creates comprehensive database for all top 300 engineering colleges in India
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


class Top300CollegesGenerator:
    """Generate data for top 300 engineering colleges in India"""
    
    def __init__(self):
        self.base_path = Path("college_data")
        self.base_path.mkdir(exist_ok=True)
        
        # Initialize comprehensive college database
        self.all_colleges = {}
        self.load_all_college_categories()
    
    def load_all_college_categories(self):
        """Load all categories of engineering colleges"""
        
        # Add all categories
        self.all_colleges.update(self.get_all_23_iits())
        self.all_colleges.update(self.get_all_31_nits())
        self.all_colleges.update(self.get_all_iiiits())
        self.all_colleges.update(self.get_top_private_universities())
        self.all_colleges.update(self.get_state_government_colleges())
        self.all_colleges.update(self.get_deemed_universities())
        self.all_colleges.update(self.get_central_universities())
        self.all_colleges.update(self.get_autonomous_colleges())
        self.all_colleges.update(self.get_specialized_institutions())
        
        print(f"📊 Total colleges loaded: {len(self.all_colleges)}")
    
    def get_all_23_iits(self) -> Dict[str, Dict[str, Any]]:
        """All 23 IITs with latest data"""
        
        iits = {
            "IIT Madras": {
                "name": "Indian Institute of Technology Madras",
                "established": 1959, "state": "Tamil Nadu", "city": "Chennai",
                "nirf_rank": 1, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Delhi": {
                "name": "Indian Institute of Technology Delhi",
                "established": 1961, "state": "Delhi", "city": "New Delhi", 
                "nirf_rank": 2, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Bombay": {
                "name": "Indian Institute of Technology Bombay",
                "established": 1958, "state": "Maharashtra", "city": "Mumbai",
                "nirf_rank": 3, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Kanpur": {
                "name": "Indian Institute of Technology Kanpur",
                "established": 1959, "state": "Uttar Pradesh", "city": "Kanpur",
                "nirf_rank": 4, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Kharagpur": {
                "name": "Indian Institute of Technology Kharagpur",
                "established": 1951, "state": "West Bengal", "city": "Kharagpur",
                "nirf_rank": 5, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Roorkee": {
                "name": "Indian Institute of Technology Roorkee",
                "established": 1847, "state": "Uttarakhand", "city": "Roorkee",
                "nirf_rank": 6, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Guwahati": {
                "name": "Indian Institute of Technology Guwahati",
                "established": 1994, "state": "Assam", "city": "Guwahati",
                "nirf_rank": 7, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Hyderabad": {
                "name": "Indian Institute of Technology Hyderabad",
                "established": 2008, "state": "Telangana", "city": "Hyderabad",
                "nirf_rank": 8, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Indore": {
                "name": "Indian Institute of Technology Indore",
                "established": 2009, "state": "Madhya Pradesh", "city": "Indore",
                "nirf_rank": 16, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT BHU": {
                "name": "Indian Institute of Technology (BHU) Varanasi",
                "established": 1919, "state": "Uttar Pradesh", "city": "Varanasi",
                "nirf_rank": 10, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Gandhinagar": {
                "name": "Indian Institute of Technology Gandhinagar",
                "established": 2008, "state": "Gujarat", "city": "Gandhinagar",
                "nirf_rank": 18, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Ropar": {
                "name": "Indian Institute of Technology Ropar",
                "established": 2008, "state": "Punjab", "city": "Rupnagar",
                "nirf_rank": 31, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Patna": {
                "name": "Indian Institute of Technology Patna",
                "established": 2008, "state": "Bihar", "city": "Patna",
                "nirf_rank": 32, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Mandi": {
                "name": "Indian Institute of Technology Mandi",
                "established": 2009, "state": "Himachal Pradesh", "city": "Mandi",
                "nirf_rank": 42, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Jodhpur": {
                "name": "Indian Institute of Technology Jodhpur",
                "established": 2008, "state": "Rajasthan", "city": "Jodhpur",
                "nirf_rank": 43, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Bhubaneswar": {
                "name": "Indian Institute of Technology Bhubaneswar",
                "established": 2008, "state": "Odisha", "city": "Bhubaneswar",
                "nirf_rank": 47, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Tirupati": {
                "name": "Indian Institute of Technology Tirupati",
                "established": 2015, "state": "Andhra Pradesh", "city": "Tirupati",
                "nirf_rank": 58, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Palakkad": {
                "name": "Indian Institute of Technology Palakkad",
                "established": 2015, "state": "Kerala", "city": "Palakkad",
                "nirf_rank": 65, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Jammu": {
                "name": "Indian Institute of Technology Jammu",
                "established": 2016, "state": "Jammu and Kashmir", "city": "Jammu",
                "nirf_rank": 72, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Goa": {
                "name": "Indian Institute of Technology Goa",
                "established": 2016, "state": "Goa", "city": "Ponda",
                "nirf_rank": 78, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Bhilai": {
                "name": "Indian Institute of Technology Bhilai",
                "established": 2016, "state": "Chhattisgarh", "city": "Bhilai",
                "nirf_rank": 85, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Dharwad": {
                "name": "Indian Institute of Technology Dharwad",
                "established": 2016, "state": "Karnataka", "city": "Dharwad",
                "nirf_rank": 89, "fees": 250000, "type": "Central Government", "category": "IIT"
            },
            "IIT Dhanbad": {
                "name": "Indian Institute of Technology (ISM) Dhanbad",
                "established": 1926, "state": "Jharkhand", "city": "Dhanbad",
                "nirf_rank": 35, "fees": 250000, "type": "Central Government", "category": "IIT"
            }
        }
        
        return iits
    
    def get_all_31_nits(self) -> Dict[str, Dict[str, Any]]:
        """All 31 NITs with comprehensive data"""
        
        nits = {
            "NIT Trichy": {
                "name": "National Institute of Technology Tiruchirappalli",
                "established": 1964, "state": "Tamil Nadu", "city": "Tiruchirappalli",
                "nirf_rank": 9, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Surathkal": {
                "name": "National Institute of Technology Karnataka",
                "established": 1960, "state": "Karnataka", "city": "Surathkal",
                "nirf_rank": 13, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Warangal": {
                "name": "National Institute of Technology Warangal",
                "established": 1959, "state": "Telangana", "city": "Warangal",
                "nirf_rank": 19, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Calicut": {
                "name": "National Institute of Technology Calicut",
                "established": 1961, "state": "Kerala", "city": "Calicut",
                "nirf_rank": 23, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Rourkela": {
                "name": "National Institute of Technology Rourkela",
                "established": 1961, "state": "Odisha", "city": "Rourkela",
                "nirf_rank": 24, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Kurukshetra": {
                "name": "National Institute of Technology Kurukshetra",
                "established": 1963, "state": "Haryana", "city": "Kurukshetra",
                "nirf_rank": 40, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Jaipur": {
                "name": "Malaviya National Institute of Technology Jaipur",
                "established": 1963, "state": "Rajasthan", "city": "Jaipur",
                "nirf_rank": 45, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Allahabad": {
                "name": "Motilal Nehru National Institute of Technology Allahabad",
                "established": 1961, "state": "Uttar Pradesh", "city": "Prayagraj",
                "nirf_rank": 48, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Bhopal": {
                "name": "National Institute of Technology Bhopal",
                "established": 1960, "state": "Madhya Pradesh", "city": "Bhopal",
                "nirf_rank": 52, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Nagpur": {
                "name": "Visvesvaraya National Institute of Technology Nagpur",
                "established": 1960, "state": "Maharashtra", "city": "Nagpur",
                "nirf_rank": 54, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Durgapur": {
                "name": "National Institute of Technology Durgapur",
                "established": 1960, "state": "West Bengal", "city": "Durgapur",
                "nirf_rank": 56, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Jamshedpur": {
                "name": "National Institute of Technology Jamshedpur",
                "established": 1960, "state": "Jharkhand", "city": "Jamshedpur",
                "nirf_rank": 59, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Hamirpur": {
                "name": "National Institute of Technology Hamirpur",
                "established": 1986, "state": "Himachal Pradesh", "city": "Hamirpur",
                "nirf_rank": 62, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Jalandhar": {
                "name": "Dr. B R Ambedkar National Institute of Technology Jalandhar",
                "established": 1987, "state": "Punjab", "city": "Jalandhar",
                "nirf_rank": 64, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Patna": {
                "name": "National Institute of Technology Patna",
                "established": 1886, "state": "Bihar", "city": "Patna",
                "nirf_rank": 67, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Raipur": {
                "name": "National Institute of Technology Raipur",
                "established": 1956, "state": "Chhattisgarh", "city": "Raipur",
                "nirf_rank": 69, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Agartala": {
                "name": "National Institute of Technology Agartala",
                "established": 1965, "state": "Tripura", "city": "Agartala",
                "nirf_rank": 71, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Silchar": {
                "name": "National Institute of Technology Silchar",
                "established": 1967, "state": "Assam", "city": "Silchar",
                "nirf_rank": 73, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Arunachal Pradesh": {
                "name": "National Institute of Technology Arunachal Pradesh",
                "established": 2010, "state": "Arunachal Pradesh", "city": "Yupia",
                "nirf_rank": 75, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Delhi": {
                "name": "National Institute of Technology Delhi",
                "established": 2010, "state": "Delhi", "city": "New Delhi",
                "nirf_rank": 77, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Goa": {
                "name": "National Institute of Technology Goa",
                "established": 2010, "state": "Goa", "city": "Farmagudi",
                "nirf_rank": 79, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Manipur": {
                "name": "National Institute of Technology Manipur",
                "established": 2010, "state": "Manipur", "city": "Imphal",
                "nirf_rank": 81, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Meghalaya": {
                "name": "National Institute of Technology Meghalaya",
                "established": 2010, "state": "Meghalaya", "city": "Shillong",
                "nirf_rank": 83, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Mizoram": {
                "name": "National Institute of Technology Mizoram",
                "established": 2010, "state": "Mizoram", "city": "Aizawl",
                "nirf_rank": 87, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Nagaland": {
                "name": "National Institute of Technology Nagaland",
                "established": 2010, "state": "Nagaland", "city": "Dimapur",
                "nirf_rank": 91, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Puducherry": {
                "name": "National Institute of Technology Puducherry",
                "established": 2010, "state": "Puducherry", "city": "Karaikal",
                "nirf_rank": 93, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Sikkim": {
                "name": "National Institute of Technology Sikkim",
                "established": 2010, "state": "Sikkim", "city": "Ravangla",
                "nirf_rank": 95, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Srinagar": {
                "name": "National Institute of Technology Srinagar",
                "established": 1960, "state": "Jammu and Kashmir", "city": "Srinagar",
                "nirf_rank": 97, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Tadepalligudem": {
                "name": "National Institute of Technology Andhra Pradesh",
                "established": 2015, "state": "Andhra Pradesh", "city": "Tadepalligudem",
                "nirf_rank": 99, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Uttarakhand": {
                "name": "National Institute of Technology Uttarakhand",
                "established": 2009, "state": "Uttarakhand", "city": "Srinagar",
                "nirf_rank": 101, "fees": 125000, "type": "Central Government", "category": "NIT"
            },
            "NIT Karnataka": {
                "name": "National Institute of Technology Karnataka Surathkal",
                "established": 1960, "state": "Karnataka", "city": "Surathkal",
                "nirf_rank": 13, "fees": 125000, "type": "Central Government", "category": "NIT"
            }
        }
        
        return nits

    def get_all_iiiits(self) -> Dict[str, Dict[str, Any]]:
        """All major IIITs and related institutions"""

        iiiits = {
            "IIIT Hyderabad": {
                "name": "International Institute of Information Technology Hyderabad",
                "established": 1998, "state": "Telangana", "city": "Hyderabad",
                "nirf_rank": 44, "fees": 350000, "type": "Private Deemed", "category": "IIIT"
            },
            "IIIT Bangalore": {
                "name": "International Institute of Information Technology Bangalore",
                "established": 1999, "state": "Karnataka", "city": "Bangalore",
                "nirf_rank": 52, "fees": 320000, "type": "Private Deemed", "category": "IIIT"
            },
            "IIIT Delhi": {
                "name": "Indraprastha Institute of Information Technology Delhi",
                "established": 2008, "state": "Delhi", "city": "New Delhi",
                "nirf_rank": 61, "fees": 300000, "type": "State Government", "category": "IIIT"
            },
            "IIIT Allahabad": {
                "name": "Indian Institute of Information Technology Allahabad",
                "established": 1999, "state": "Uttar Pradesh", "city": "Prayagraj",
                "nirf_rank": 103, "fees": 280000, "type": "Central Government", "category": "IIIT"
            },
            "IIIT Gwalior": {
                "name": "ABV-Indian Institute of Information Technology and Management Gwalior",
                "established": 1997, "state": "Madhya Pradesh", "city": "Gwalior",
                "nirf_rank": 105, "fees": 275000, "type": "Central Government", "category": "IIIT"
            },
            "IIIT Jabalpur": {
                "name": "Pandit Dwarka Prasad Mishra Indian Institute of Information Technology Design and Manufacturing Jabalpur",
                "established": 2005, "state": "Madhya Pradesh", "city": "Jabalpur",
                "nirf_rank": 107, "fees": 270000, "type": "Central Government", "category": "IIIT"
            },
            "IIIT Kancheepuram": {
                "name": "Indian Institute of Information Technology Design and Manufacturing Kancheepuram",
                "established": 2007, "state": "Tamil Nadu", "city": "Chennai",
                "nirf_rank": 109, "fees": 265000, "type": "Central Government", "category": "IIIT"
            },
            "IIIT Lucknow": {
                "name": "Indian Institute of Information Technology Lucknow",
                "established": 2015, "state": "Uttar Pradesh", "city": "Lucknow",
                "nirf_rank": 111, "fees": 260000, "type": "Central Government", "category": "IIIT"
            },
            "IIIT Vadodara": {
                "name": "Indian Institute of Information Technology Vadodara",
                "established": 2013, "state": "Gujarat", "city": "Gandhinagar",
                "nirf_rank": 113, "fees": 255000, "type": "Central Government", "category": "IIIT"
            },
            "IIIT Nagpur": {
                "name": "Visvesvaraya National Institute of Technology Nagpur",
                "established": 2016, "state": "Maharashtra", "city": "Nagpur",
                "nirf_rank": 115, "fees": 250000, "type": "Central Government", "category": "IIIT"
            },
            "IISc Bangalore": {
                "name": "Indian Institute of Science Bangalore",
                "established": 1909, "state": "Karnataka", "city": "Bangalore",
                "nirf_rank": 1, "fees": 200000, "type": "Central Government", "category": "IISc"
            }
        }

        return iiiits

    def get_top_private_universities(self) -> Dict[str, Dict[str, Any]]:
        """Top 50 private engineering universities"""

        private_unis = {
            "BITS Pilani": {
                "name": "Birla Institute of Technology and Science Pilani",
                "established": 1964, "state": "Rajasthan", "city": "Pilani",
                "nirf_rank": 25, "fees": 450000, "type": "Private Deemed", "category": "Private"
            },
            "VIT Vellore": {
                "name": "Vellore Institute of Technology",
                "established": 1984, "state": "Tamil Nadu", "city": "Vellore",
                "nirf_rank": 15, "fees": 400000, "type": "Private Deemed", "category": "Private"
            },
            "Thapar University": {
                "name": "Thapar Institute of Engineering and Technology",
                "established": 1956, "state": "Punjab", "city": "Patiala",
                "nirf_rank": 29, "fees": 420000, "type": "Private Deemed", "category": "Private"
            },
            "Manipal Institute of Technology": {
                "name": "Manipal Institute of Technology",
                "established": 1957, "state": "Karnataka", "city": "Manipal",
                "nirf_rank": 48, "fees": 380000, "type": "Private Deemed", "category": "Private"
            },
            "SRM Chennai": {
                "name": "SRM Institute of Science and Technology",
                "established": 1985, "state": "Tamil Nadu", "city": "Chennai",
                "nirf_rank": 41, "fees": 350000, "type": "Private Deemed", "category": "Private"
            },
            "Amity University Noida": {
                "name": "Amity University Uttar Pradesh",
                "established": 2005, "state": "Uttar Pradesh", "city": "Noida",
                "nirf_rank": 68, "fees": 320000, "type": "Private University", "category": "Private"
            },
            "LPU Punjab": {
                "name": "Lovely Professional University",
                "established": 2005, "state": "Punjab", "city": "Phagwara",
                "nirf_rank": 70, "fees": 280000, "type": "Private University", "category": "Private"
            },
            "Chitkara University": {
                "name": "Chitkara University Punjab",
                "established": 2010, "state": "Punjab", "city": "Rajpura",
                "nirf_rank": 74, "fees": 300000, "type": "Private University", "category": "Private"
            },
            "Bennett University": {
                "name": "Bennett University",
                "established": 2016, "state": "Uttar Pradesh", "city": "Greater Noida",
                "nirf_rank": 76, "fees": 450000, "type": "Private University", "category": "Private"
            },
            "Shiv Nadar University": {
                "name": "Shiv Nadar University",
                "established": 2011, "state": "Uttar Pradesh", "city": "Greater Noida",
                "nirf_rank": 80, "fees": 480000, "type": "Private University", "category": "Private"
            },
            "KIIT University": {
                "name": "Kalinga Institute of Industrial Technology",
                "established": 1992, "state": "Odisha", "city": "Bhubaneswar",
                "nirf_rank": 82, "fees": 320000, "type": "Private Deemed", "category": "Private"
            },
            "VIT Chennai": {
                "name": "VIT University Chennai",
                "established": 2010, "state": "Tamil Nadu", "city": "Chennai",
                "nirf_rank": 84, "fees": 380000, "type": "Private Deemed", "category": "Private"
            },
            "Symbiosis International University": {
                "name": "Symbiosis Institute of Technology",
                "established": 2008, "state": "Maharashtra", "city": "Pune",
                "nirf_rank": 86, "fees": 350000, "type": "Private Deemed", "category": "Private"
            },
            "SASTRA University": {
                "name": "Shanmugha Arts Science Technology and Research Academy",
                "established": 1984, "state": "Tamil Nadu", "city": "Thanjavur",
                "nirf_rank": 88, "fees": 280000, "type": "Private Deemed", "category": "Private"
            },
            "SSN College of Engineering": {
                "name": "Sri Sivasubramaniya Nadar College of Engineering",
                "established": 1996, "state": "Tamil Nadu", "city": "Chennai",
                "nirf_rank": 90, "fees": 250000, "type": "Private Autonomous", "category": "Private"
            }
        }

        return private_unis
