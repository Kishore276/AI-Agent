"""
Complete Data Generator for All Colleges
Creates comprehensive JSON files following Kalasalingam University structure
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

# College information database
COLLEGES_DATABASE = {
    # IITs
    "IIT Bombay": {"type": "IIT", "state": "Maharashtra", "city": "Mumbai", "rank": 3, "established": 1958},
    "IIT Delhi": {"type": "IIT", "state": "Delhi", "city": "New Delhi", "rank": 2, "established": 1961},
    "IIT Madras": {"type": "IIT", "state": "Tamil Nadu", "city": "Chennai", "rank": 1, "established": 1959},
    "IIT Kanpur": {"type": "IIT", "state": "Uttar Pradesh", "city": "Kanpur", "rank": 4, "established": 1959},
    "IIT Kharagpur": {"type": "IIT", "state": "West Bengal", "city": "Kharagpur", "rank": 5, "established": 1951},
    "IIT Roorkee": {"type": "IIT", "state": "Uttarakhand", "city": "Roorkee", "rank": 6, "established": 1847},
    "IIT Guwahati": {"type": "IIT", "state": "Assam", "city": "Guwahati", "rank": 7, "established": 1994},
    "IIT Hyderabad": {"type": "IIT", "state": "Telangana", "city": "Hyderabad", "rank": 8, "established": 2008},
    "IIT Indore": {"type": "IIT", "state": "Madhya Pradesh", "city": "Indore", "rank": 16, "established": 2009},
    
    # NITs
    "NIT Trichy": {"type": "NIT", "state": "Tamil Nadu", "city": "Tiruchirappalli", "rank": 9, "established": 1964},
    "NIT Surathkal": {"type": "NIT", "state": "Karnataka", "city": "Surathkal", "rank": 10, "established": 1960},
    "NIT Warangal": {"type": "NIT", "state": "Telangana", "city": "Warangal", "rank": 19, "established": 1959},
    "NIT Calicut": {"type": "NIT", "state": "Kerala", "city": "Calicut", "rank": 23, "established": 1961},
    "NIT Rourkela": {"type": "NIT", "state": "Odisha", "city": "Rourkela", "rank": 16, "established": 1961},
    
    # IIITs
    "IIIT Hyderabad": {"type": "IIIT", "state": "Telangana", "city": "Hyderabad", "rank": 25, "established": 1998},
    "IIIT Bangalore": {"type": "IIIT", "state": "Karnataka", "city": "Bangalore", "rank": 35, "established": 1999},
    
    # Private Universities
    "BITS Pilani": {"type": "Private", "state": "Rajasthan", "city": "Pilani", "rank": 30, "established": 1964},
    "VIT Vellore": {"type": "Private", "state": "Tamil Nadu", "city": "Vellore", "rank": 15, "established": 1984},
    "SRM Chennai": {"type": "Private", "state": "Tamil Nadu", "city": "Chennai", "rank": 35, "established": 1985},
    "Manipal Institute of Technology": {"type": "Private", "state": "Karnataka", "city": "Manipal", "rank": 45, "established": 1957},
    "Thapar University": {"type": "Private", "state": "Punjab", "city": "Patiala", "rank": 29, "established": 1956},
    
    # State Universities
    "Anna University": {"type": "State", "state": "Tamil Nadu", "city": "Chennai", "rank": 20, "established": 1978},
    "Jadavpur University": {"type": "State", "state": "West Bengal", "city": "Kolkata", "rank": 12, "established": 1955}
}

def create_all_files():
    """Create all missing files for all colleges"""
    base_path = Path("college_data")
    
    for college_name, info in COLLEGES_DATABASE.items():
        college_path = base_path / college_name
        college_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🏫 Processing {college_name}...")
        
        # Check which files are missing
        required_files = ["basic_info.json", "courses.json", "fees_structure.json", 
                         "admission_process.json", "facilities.json", "placements.json", "faq.json"]
        
        for file_name in required_files:
            file_path = college_path / file_name
            if not file_path.exists():
                print(f"   Creating {file_name}...")
                content = generate_file_content(college_name, file_name, info)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
                print(f"   ✅ Created {file_name}")
            else:
                print(f"   ⏭️ {file_name} already exists")

def generate_file_content(college_name: str, file_name: str, info: Dict) -> Dict:
    """Generate content for specific file type"""
    
    if file_name == "courses.json":
        return generate_courses_content(college_name, info)
    elif file_name == "admission_process.json":
        return generate_admission_content(college_name, info)
    elif file_name == "facilities.json":
        return generate_facilities_content(college_name, info)
    elif file_name == "placements.json":
        return generate_placements_content(college_name, info)
    elif file_name == "faq.json":
        return generate_faq_content(college_name, info)
    elif file_name == "fees_structure.json":
        return generate_fees_content(college_name, info)
    else:
        return {}

def generate_courses_content(college_name: str, info: Dict) -> Dict:
    """Generate courses.json content"""
    college_type = info["type"]
    
    # Base departments for all colleges
    departments = [
        {
            "name": "Computer Science and Engineering",
            "code": "CSE",
            "specializations": ["Artificial Intelligence", "Data Science", "Software Engineering", "Cyber Security"],
            "intake": 120 if college_type == "IIT" else 180,
            "faculty_count": 65 if college_type == "IIT" else 45,
            "labs": ["Programming Lab", "AI Lab", "Database Lab", "Networks Lab"]
        },
        {
            "name": "Electronics and Communication Engineering",
            "code": "ECE", 
            "specializations": ["VLSI Design", "Communication Systems", "Signal Processing", "Embedded Systems"],
            "intake": 120 if college_type == "IIT" else 120,
            "faculty_count": 55 if college_type == "IIT" else 35,
            "labs": ["Electronics Lab", "Communication Lab", "VLSI Lab", "Microprocessor Lab"]
        },
        {
            "name": "Mechanical Engineering",
            "code": "ME",
            "specializations": ["Thermal Engineering", "Design and Manufacturing", "Robotics", "Automobile"],
            "intake": 120 if college_type == "IIT" else 120,
            "faculty_count": 60 if college_type == "IIT" else 40,
            "labs": ["Manufacturing Lab", "Thermal Lab", "CAD Lab", "Robotics Lab"]
        }
    ]
    
    # Add more departments for IITs
    if college_type == "IIT":
        departments.extend([
            {
                "name": "Civil Engineering",
                "code": "CE",
                "specializations": ["Structural", "Environmental", "Transportation", "Geotechnical"],
                "intake": 80,
                "faculty_count": 45,
                "labs": ["Structural Lab", "Environmental Lab", "Geotechnical Lab"]
            },
            {
                "name": "Chemical Engineering", 
                "code": "ChE",
                "specializations": ["Process Engineering", "Biochemical", "Materials"],
                "intake": 80,
                "faculty_count": 40,
                "labs": ["Process Lab", "Biochemical Lab", "Materials Lab"]
            }
        ])
    
    return {
        "undergraduate_programs": {
            "engineering": {
                "btech": {
                    "duration": "4 years",
                    "total_semesters": 8,
                    "eligibility": "JEE Advanced qualified" if college_type == "IIT" else "JEE Main qualified",
                    "admission_process": ["JEE Advanced"] if college_type == "IIT" else ["JEE Main", "State CET"],
                    "departments": departments
                }
            }
        },
        "postgraduate_programs": {
            "mtech": {
                "duration": "2 years",
                "admission": "GATE qualified",
                "programs": [
                    {"name": "Computer Science and Engineering", "specializations": ["AI & ML", "Systems"], "intake": 50},
                    {"name": "Electrical Engineering", "specializations": ["Power Systems", "VLSI"], "intake": 40}
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

def generate_fees_content(college_name: str, info: Dict) -> Dict:
    """Generate fees_structure.json content"""
    college_type = info["type"]

    # Base fees vary by college type
    if college_type == "IIT":
        btech_fee = 250000
        hostel_fee = 18000
        mess_fee = 45000
    elif college_type == "NIT":
        btech_fee = 150000
        hostel_fee = 15000
        mess_fee = 35000
    elif college_type == "Private":
        btech_fee = 300000
        hostel_fee = 80000
        mess_fee = 50000
    else:  # State
        btech_fee = 100000
        hostel_fee = 25000
        mess_fee = 30000

    return {
        "academic_year": "2025-2026",
        "currency": "INR",
        "undergraduate": {
            "btech": {
                "tuition_fee_per_year": btech_fee,
                "other_fees": {
                    "admission_fee": 5000 if college_type == "Private" else 0,
                    "caution_deposit": 5000,
                    "exam_fee": 3000,
                    "library_fee": 2000,
                    "lab_fee": 5000,
                    "sports_fee": 1000
                },
                "total_per_year": btech_fee + 21000,
                "payment_schedule": {
                    "semester_wise": "Payment every semester"
                }
            }
        },
        "postgraduate": {
            "mtech": {
                "tuition_fee_per_year": btech_fee // 5,
                "total_per_year": (btech_fee // 5) + 15000
            }
        },
        "hostel_fees": {
            "accommodation_per_year": hostel_fee,
            "mess_fee_per_year": mess_fee,
            "total_per_year": hostel_fee + mess_fee
        },
        "scholarships": {
            "merit_based": [
                {
                    "name": "Merit Scholarship",
                    "criteria": "Top 10% students",
                    "benefit": "50% tuition fee waiver"
                }
            ]
        }
    }

def generate_admission_content(college_name: str, info: Dict) -> Dict:
    """Generate admission_process.json content"""
    college_type = info["type"]

    if college_type == "IIT":
        entrance_exam = "JEE Advanced"
        cutoff_rank = 100 * info["rank"]
    elif college_type in ["NIT", "IIIT"]:
        entrance_exam = "JEE Main"
        cutoff_rank = 1000 * info["rank"]
    else:
        entrance_exam = "Entrance Exam"
        cutoff_rank = 5000

    return {
        "admission_year": "2025-2026",
        "entrance_exams": {
            "primary_exam": {
                "name": entrance_exam,
                "mode": "Computer Based Test",
                "cutoff_rank": cutoff_rank
            }
        },
        "important_dates_2025": {
            "application_start": "2025-03-01",
            "application_end": "2025-04-30",
            "exam_date": "2025-05-15",
            "result_date": "2025-06-01",
            "counseling_start": "2025-06-15"
        },
        "eligibility_criteria": {
            "btech": {
                "academic": "10+2 with PCM",
                "minimum_percentage": 75 if college_type == "IIT" else 60,
                "age_limit": "25 years"
            }
        },
        "seat_matrix": {
            "total_seats": 800 if college_type == "IIT" else 600,
            "category_wise": {
                "general": 400,
                "obc": 200,
                "sc": 120,
                "st": 80
            }
        }
    }

def generate_facilities_content(college_name: str, info: Dict) -> Dict:
    """Generate facilities.json content"""
    college_type = info["type"]

    return {
        "academic_facilities": {
            "libraries": {
                "central_library": {
                    "name": "Central Library",
                    "area_sqft": 60000 if college_type == "IIT" else 40000,
                    "books": 400000 if college_type == "IIT" else 200000,
                    "journals": 2000 if college_type == "IIT" else 1000,
                    "e_books": 150000 if college_type == "IIT" else 80000,
                    "digital_resources": ["IEEE Xplore", "ACM Digital Library", "Springer"],
                    "seating_capacity": 1000 if college_type == "IIT" else 600,
                    "working_hours": "24x7"
                }
            },
            "laboratories": {
                "total_labs": 150 if college_type == "IIT" else 100,
                "computer_labs": 25,
                "engineering_labs": 60,
                "research_labs": 20 if college_type == "IIT" else 10
            },
            "classrooms": {
                "total_classrooms": 150,
                "smart_classrooms": 100,
                "lecture_halls": 20,
                "auditoriums": 3
            }
        },
        "hostel_facilities": {
            "boys_hostels": {
                "count": 8,
                "total_capacity": 3000,
                "amenities": ["24x7 Wi-Fi", "Laundry", "Gym", "Security"]
            },
            "girls_hostels": {
                "count": 4,
                "total_capacity": 1500,
                "amenities": ["24x7 Wi-Fi", "Laundry", "Gym", "Security"]
            }
        },
        "sports_facilities": {
            "outdoor_sports": {
                "cricket_ground": {"count": 2},
                "football_field": {"count": 1},
                "basketball_courts": {"count": 4},
                "tennis_courts": {"count": 6}
            },
            "indoor_sports": {
                "gymnasium": {"area_sqft": 5000},
                "swimming_pool": {"type": "Olympic Size"}
            }
        },
        "other_facilities": {
            "medical": {"type": "24x7 Medical Center"},
            "banking": {"banks": ["SBI", "Canara Bank"], "atms": 5},
            "transportation": {"bus_routes": 15, "campus_shuttle": True}
        }
    }

def generate_placements_content(college_name: str, info: Dict) -> Dict:
    """Generate placements.json content"""
    college_type = info["type"]

    # Placement stats vary by college type and ranking
    if college_type == "IIT":
        placement_rate = 95 + (10 - info["rank"]) if info["rank"] <= 10 else 90
        avg_package = 25 - info["rank"] if info["rank"] <= 10 else 15
        highest_package = 180 if info["rank"] <= 5 else 100
    elif college_type == "NIT":
        placement_rate = 85
        avg_package = 12
        highest_package = 50
    elif college_type == "Private":
        placement_rate = 90
        avg_package = 10
        highest_package = 60
    else:  # State
        placement_rate = 80
        avg_package = 8
        highest_package = 30

    return {
        "placement_statistics": {
            "academic_year": "2024-2025",
            "overall_placement_percentage": placement_rate,
            "total_students_placed": 1500,
            "highest_package_lpa": highest_package,
            "average_package_lpa": avg_package,
            "median_package_lpa": avg_package * 0.8
        },
        "department_wise_placements": {
            "computer_science": {
                "placement_percentage": min(placement_rate + 5, 100),
                "average_package": avg_package * 1.5,
                "top_recruiters": ["Google", "Microsoft", "Amazon", "TCS", "Infosys"]
            },
            "electronics_communication": {
                "placement_percentage": placement_rate,
                "average_package": avg_package * 1.2,
                "top_recruiters": ["Intel", "Qualcomm", "Samsung", "Wipro"]
            }
        },
        "top_recruiters": {
            "tier_1_companies": [
                {"name": "Google", "packages_offered": f"{avg_package*3}-{highest_package} LPA"},
                {"name": "Microsoft", "packages_offered": f"{avg_package*2.5}-{highest_package*0.8} LPA"}
            ]
        },
        "alumni_network": {
            "total_alumni": 30000,
            "countries": 50 if college_type == "IIT" else 25
        }
    }

def generate_faq_content(college_name: str, info: Dict) -> Dict:
    """Generate faq.json content"""
    college_type = info["type"]

    return {
        "frequently_asked_questions": {
            "admission_related": [
                {
                    "question": f"What is the eligibility criteria for admission to {college_name}?",
                    "answer": f"Candidates must qualify {('JEE Advanced' if college_type == 'IIT' else 'JEE Main')} and have 10+2 with PCM with minimum {('75%' if college_type == 'IIT' else '60%')} marks."
                },
                {
                    "question": f"What is the cutoff rank for {college_name}?",
                    "answer": f"Cutoff ranks vary by branch and category. For CSE, the general category cutoff is typically around {100 * info['rank'] if college_type == 'IIT' else 1000 * info['rank']}."
                },
                {
                    "question": "What documents are required for admission?",
                    "answer": "10th & 12th certificates, entrance exam scorecard, category certificate (if applicable), and other standard documents."
                }
            ],
            "fee_related": [
                {
                    "question": f"What is the fee structure at {college_name}?",
                    "answer": f"The annual fee is approximately INR {('2.5-3 lakhs' if college_type == 'IIT' else '1.5-3 lakhs depending on the program')} including hostel and mess charges."
                },
                {
                    "question": "Are scholarships available?",
                    "answer": "Yes, merit-based and need-based scholarships are available. SC/ST students get fee concessions as per government norms."
                }
            ],
            "placement_related": [
                {
                    "question": f"What is the placement record of {college_name}?",
                    "answer": f"The college has excellent placement record with {('95%+' if college_type == 'IIT' else '85-90%')} placement rate and top companies visiting campus."
                },
                {
                    "question": "Which companies visit for placements?",
                    "answer": f"Top companies like {('Google, Microsoft, Amazon' if college_type == 'IIT' else 'TCS, Infosys, Wipro')}, and many Fortune 500 companies visit for placements."
                }
            ],
            "general_queries": [
                {
                    "question": f"Where is {college_name} located?",
                    "answer": f"{college_name} is located in {info['city']}, {info['state']}, India."
                },
                {
                    "question": "What facilities are available on campus?",
                    "answer": "The campus has excellent academic facilities, hostels, sports complex, medical center, and all modern amenities."
                }
            ]
        }
    }

if __name__ == "__main__":
    print("🎓 Complete College Data Generator")
    print("=" * 50)
    create_all_files()
    print("\n🎉 All files generated successfully!")
