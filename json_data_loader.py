"""
JSON Data Loader for Kalasalingam University Chatbot
This script loads comprehensive college data from JSON files and converts them to text format
for use with the RAG (Retrieval Augmented Generation) system.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any


class CollegeDataLoader:
    """Load and process college data from JSON files"""
    
    def __init__(self, data_directory: str = "college_data"):
        self.data_directory = Path(data_directory)
        self.loaded_data = {}
        
    def load_all_json_files(self) -> Dict[str, Any]:
        """Load all JSON files from the data directory"""
        
        if not self.data_directory.exists():
            raise FileNotFoundError(f"Data directory {self.data_directory} not found")
        
        json_files = list(self.data_directory.glob("*.json"))
        
        if not json_files:
            raise FileNotFoundError(f"No JSON files found in {self.data_directory}")
        
        for json_file in json_files:
            file_key = json_file.stem  # filename without extension
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.loaded_data[file_key] = json.load(f)
                print(f"✅ Loaded: {json_file.name}")
            except Exception as e:
                print(f"❌ Error loading {json_file.name}: {e}")
        
        return self.loaded_data
    
    def json_to_text(self, data: Dict[str, Any], title: str = "") -> str:
        """Convert JSON data to formatted text"""
        
        def format_value(value, indent_level=0):
            """Recursively format JSON values to text"""
            indent = "  " * indent_level
            
            if isinstance(value, dict):
                lines = []
                for key, val in value.items():
                    formatted_key = key.replace('_', ' ').title()
                    if isinstance(val, (dict, list)):
                        lines.append(f"{indent}{formatted_key}:")
                        lines.append(format_value(val, indent_level + 1))
                    else:
                        lines.append(f"{indent}{formatted_key}: {val}")
                return "\n".join(lines)
            
            elif isinstance(value, list):
                lines = []
                for item in value:
                    if isinstance(item, dict):
                        lines.append(format_value(item, indent_level))
                    else:
                        lines.append(f"{indent}- {item}")
                return "\n".join(lines)
            
            else:
                return f"{indent}{value}"
        
        # Create formatted text
        text_content = []
        if title:
            text_content.append(f"# {title}\n")
        
        text_content.append(format_value(data))
        
        return "\n".join(text_content)
    
    def create_text_files(self, output_directory: str = "processed_data") -> List[str]:
        """Convert all JSON files to text files"""
        
        if not self.loaded_data:
            self.load_all_json_files()
        
        output_path = Path(output_directory)
        output_path.mkdir(exist_ok=True)
        
        created_files = []
        
        for file_key, data in self.loaded_data.items():
            # Create title from filename
            title = file_key.replace('_', ' ').title()
            
            # Convert to text
            text_content = self.json_to_text(data, title)
            
            # Save as text file
            output_file = output_path / f"{file_key}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            created_files.append(str(output_file))
            print(f"📝 Created: {output_file.name}")
        
        return created_files
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of loaded data"""
        
        if not self.loaded_data:
            self.load_all_json_files()
        
        summary = {
            "total_files": len(self.loaded_data),
            "files": list(self.loaded_data.keys()),
            "data_categories": {}
        }
        
        for file_key, data in self.loaded_data.items():
            if isinstance(data, dict):
                summary["data_categories"][file_key] = list(data.keys())
        
        return summary


def integrate_with_existing_notebook():
    """
    Integration code to add to your existing Colab notebook
    """
    
    integration_code = '''
# Add this code to your existing notebook to use JSON data

# 1. Upload JSON files to Colab or mount Google Drive
from google.colab import files
import zipfile

# Option A: Upload files directly
# uploaded = files.upload()

# Option B: Mount Google Drive (if files are in Drive)
# from google.colab import drive
# drive.mount('/content/drive')

# 2. Load the JSON data
from json_data_loader import CollegeDataLoader

# Initialize the data loader
data_loader = CollegeDataLoader("college_data")

# Load all JSON files
college_data = data_loader.load_all_json_files()

# Convert to text files for processing
text_files = data_loader.create_text_files("KalasalingamData_2025")

# 3. Replace the existing data creation section with:
print("📚 Loading comprehensive college data from JSON files...")

# Use DirectoryLoader to load the converted text files
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader("KalasalingamData_2025", glob="**/*.txt", show_progress=True)
documents = loader.load()

print(f"✅ Loaded {len(documents)} comprehensive documents")

# Continue with your existing text splitting and embedding code...
'''
    
    return integration_code


if __name__ == "__main__":
    # Example usage
    print("🎓 Kalasalingam University Data Loader")
    print("=" * 50)
    
    try:
        # Initialize loader
        loader = CollegeDataLoader()
        
        # Load data
        data = loader.load_all_json_files()
        
        # Create text files
        text_files = loader.create_text_files()
        
        # Show summary
        summary = loader.get_summary()
        print(f"\n📊 Data Summary:")
        print(f"Total files loaded: {summary['total_files']}")
        print(f"Categories: {', '.join(summary['files'])}")
        
        print(f"\n✅ Successfully processed {len(text_files)} files")
        print("Ready to integrate with your chatbot!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure the 'college_data' directory exists with JSON files.")
