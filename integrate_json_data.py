"""
Integration script to connect JSON data files with the existing Colab notebook
This script provides the code to replace the hardcoded data in your notebook
"""

def get_integration_code():
    """
    Returns the code to replace the data creation section in your Colab notebook
    """
    
    integration_code = '''
# Enhanced Data Loading with JSON Support
import json
import os
from pathlib import Path

def load_json_to_text(json_file_path):
    """Load JSON file and convert to formatted text"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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
    
    file_name = Path(json_file_path).stem.replace('_', ' ').title()
    content_lines = [f"# {file_name}\\n"]
    content_lines.extend(format_json_to_text(data))
    return "\\n".join(content_lines)

# Define the main data folder
folder_name = "KalasalingamData_2025"

# Create the folder if it doesn't already exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"✅ Folder '{folder_name}' created.")
else:
    print(f"Folder '{folder_name}' already exists.")

# Check if JSON files exist in college_data directory
json_data_dir = Path("college_data")
files_to_create = {}

if json_data_dir.exists() and list(json_data_dir.glob("*.json")):
    print("📚 Loading comprehensive data from JSON files...")
    json_files = list(json_data_dir.glob("*.json"))
    
    for i, json_file in enumerate(json_files, 1):
        try:
            content = load_json_to_text(json_file)
            filename = f"{i:02d}_{json_file.stem}.txt"
            files_to_create[filename] = content
            print(f"  ✅ Processed: {json_file.name}")
        except Exception as e:
            print(f"  ❌ Error processing {json_file.name}: {e}")
    
    print(f"\\n✅ Successfully loaded {len(files_to_create)} comprehensive data files!")
    
else:
    print("📝 JSON files not found in 'college_data' directory.")
    print("Using sample data instead. Upload JSON files to 'college_data' folder for comprehensive information.")
    
    # Fallback to sample data (your existing content)
    fee_content = """
# Kalasalingam University - Fee Structure 2025-2026

**B.Tech Courses (All Branches):**
- Tuition Fee per year: INR 1,60,000
- Caution Deposit (Refundable): INR 10,000
- Other Fees (Exam, Library, etc.): INR 15,000
- Total First Year Fee: INR 1,85,000

**Arts & Science (B.Sc / B.Com):**
- Tuition Fee per year: INR 50,000
- Total First Year Fee: INR 65,000

**Note:** Fees are subject to revision. Hostel and mess fees are separate.
"""

    cse_details_content = """
# B.Tech - Computer Science and Engineering (CSE) Details 2025

**Duration:** 4 Years (8 Semesters)
**Eligibility:** A pass in 10+2 (or equivalent) with a minimum of 60% aggregate in Mathematics, Physics, and Chemistry.
**Mode of Admission:** Based on scores in KUEE (Kalasalingam University Entrance Exam) or JEE Main.

**Key Specializations Offered:**
- Artificial Intelligence and Machine Learning
- Cybersecurity
- Data Science
- Cloud Computing
"""

    hostel_content = """
# Hostel Information 2025-2026

**Facilities:**
- Separate hostels for boys and girls.
- Both AC and Non-AC rooms are available.
- 24/7 Wi-Fi connectivity.
- In-house laundry service and recreational areas.

**Fees (per year):**
- Non-AC Room (3-person sharing): INR 65,000
- AC Room (3-person sharing): INR 90,000
- Mess Fee (Mandatory for all hostel residents): INR 45,000 per year.
"""

    dates_content = """
# Important Dates - Admissions 2025

**KUEE 2025 (Phase 2):**
- Last Date to Apply: August 10, 2025
- KUEE Online Entrance Exam: August 18, 2025
- Publication of Results: August 22, 2025

**Counseling & Admission:**
- Counseling for Phase 2: August 25 - August 28, 2025
- Last Date for Admission Fee Payment: September 5, 2025
- Classes for First Year Begin: September 15, 2025
"""

    faq_content = """
# Frequently Asked Questions (FAQ) 2025

**Q: Is there a management quota for admission?**
A: For details regarding direct admission under management quota, please contact the admissions office directly at +91-XXXXX-XXXXX.

**Q: What is the cutoff for CSE based on KUEE rank?**
A: The cutoff varies each year. For Phase 1 admissions, the closing rank was around 2500. Phase 2 cutoffs will be determined after the exam.

**Q: Can I get an education loan?**
A: Yes, the university provides all necessary documentation for students to apply for education loans from nationalized and private banks.

**Q: What is the medium of instruction in the classroom?**
A: The medium of instruction for all engineering and science courses is English.
"""

    files_to_create = {
        "01_fee_structure_2025.txt": fee_content,
        "02_btech_cse_details_2025.txt": cse_details_content,
        "03_hostel_information_2025.txt": hostel_content,
        "04_important_dates_2025.txt": dates_content,
        "05_common_questions_faq.txt": faq_content,
    }

# Write the files to the directory
for filename, content in files_to_create.items():
    file_path = os.path.join(folder_name, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"- File '{filename}' created.")

print("\\n✅ All data files have been generated successfully!")
'''
    
    return integration_code

def create_upload_instructions():
    """
    Instructions for uploading JSON files to Colab
    """
    
    instructions = '''
# Instructions to Upload JSON Files to Google Colab

## Method 1: Direct Upload
1. In your Colab notebook, add this code cell:

```python
from google.colab import files
import zipfile
import os

# Upload files
uploaded = files.upload()

# If you upload a zip file containing all JSON files:
for filename in uploaded.keys():
    if filename.endswith('.zip'):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall('college_data')
        print(f"Extracted {filename} to college_data/")
    else:
        # Move individual files to college_data directory
        os.makedirs('college_data', exist_ok=True)
        os.rename(filename, f'college_data/{filename}')
        print(f"Moved {filename} to college_data/")
```

## Method 2: Google Drive
1. Upload JSON files to your Google Drive
2. Mount Google Drive in Colab:

```python
from google.colab import drive
drive.mount('/content/drive')

# Copy files from Drive to Colab
import shutil
import os

# Assuming your JSON files are in Drive/MyDrive/college_json_files/
source_dir = '/content/drive/MyDrive/college_json_files'
dest_dir = 'college_data'

os.makedirs(dest_dir, exist_ok=True)

if os.path.exists(source_dir):
    for file in os.listdir(source_dir):
        if file.endswith('.json'):
            shutil.copy2(f"{source_dir}/{file}", f"{dest_dir}/{file}")
            print(f"Copied {file}")
else:
    print("Source directory not found. Please check the path.")
```

## Method 3: GitHub (if files are in a repository)
```python
!git clone https://github.com/yourusername/your-repo.git
!cp your-repo/college_data/*.json college_data/
```

After uploading, run the enhanced data loading code to use your comprehensive JSON data!
'''
    
    return instructions

if __name__ == "__main__":
    print("🎓 JSON Data Integration for Kalasalingam Chatbot")
    print("=" * 60)
    
    print("\\n📋 Integration Code:")
    print("Replace the data creation section in your Colab notebook with this code:")
    print("-" * 60)
    print(get_integration_code())
    
    print("\\n📤 Upload Instructions:")
    print(create_upload_instructions())
