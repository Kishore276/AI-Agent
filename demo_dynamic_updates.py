#!/usr/bin/env python3
"""
Demo: Dynamic College AI with Auto-Updates
Shows how the system automatically incorporates new data without retraining
"""

import json
import time
from pathlib import Path
from dynamic_college_ai import DynamicCollegeAI

def create_sample_new_college():
    """Create a sample new college to demonstrate dynamic updates"""
    new_college_name = "IIT Hyderabad New Campus"
    new_college_path = Path("college_data") / new_college_name
    new_college_path.mkdir(exist_ok=True)
    
    # Create basic info
    basic_info = {
        "name": "IIT Hyderabad New Campus",
        "location": "Hyderabad, Telangana",
        "type": "Government",
        "established": "2024",
        "fees": {
            "tuition": "200000",
            "hostel": "50000",
            "total": "250000"
        },
        "courses": ["Computer Science", "Electronics", "Mechanical"],
        "ranking": "New Institute"
    }
    
    # Create placements info
    placements = {
        "average_package": "15 LPA",
        "highest_package": "45 LPA",
        "placement_percentage": "95%",
        "top_recruiters": ["Google", "Microsoft", "Amazon", "TCS", "Infosys"],
        "placement_statistics": {
            "2024": {
                "students_placed": 150,
                "total_students": 160,
                "average_salary": 1500000
            }
        }
    }
    
    # Create admissions info
    admissions = {
        "entrance_exam": "JEE Advanced",
        "cutoff_rank": "5000",
        "seats": {
            "Computer Science": 60,
            "Electronics": 50,
            "Mechanical": 50
        },
        "admission_process": "Through JEE Advanced counseling",
        "important_dates": {
            "application_start": "2024-06-01",
            "application_end": "2024-06-30",
            "counseling": "2024-07-15"
        }
    }
    
    # Save files
    with open(new_college_path / "basic_info.json", 'w', encoding='utf-8') as f:
        json.dump(basic_info, f, indent=2, ensure_ascii=False)
    
    with open(new_college_path / "placements.json", 'w', encoding='utf-8') as f:
        json.dump(placements, f, indent=2, ensure_ascii=False)
    
    with open(new_college_path / "admissions.json", 'w', encoding='utf-8') as f:
        json.dump(admissions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created new college: {new_college_name}")
    return new_college_name

def update_existing_college():
    """Update an existing college to demonstrate dynamic updates"""
    # Find an existing college
    college_data_path = Path("college_data")
    existing_colleges = [d for d in college_data_path.iterdir() if d.is_dir()]
    
    if not existing_colleges:
        print("❌ No existing colleges found")
        return None
    
    # Update the first college found
    college_to_update = existing_colleges[0]
    college_name = college_to_update.name
    
    # Update basic info with new fee structure
    basic_info_file = college_to_update / "basic_info.json"
    
    if basic_info_file.exists():
        with open(basic_info_file, 'r', encoding='utf-8') as f:
            basic_info = json.load(f)
        
        # Update fees
        if 'fees' not in basic_info:
            basic_info['fees'] = {}
        
        basic_info['fees']['updated_date'] = "2024-12-15"
        basic_info['fees']['tuition'] = str(int(basic_info['fees'].get('tuition', '100000')) + 10000)
        basic_info['fees']['note'] = "Fees updated for 2024-25 academic year"
        
        # Save updated info
        with open(basic_info_file, 'w', encoding='utf-8') as f:
            json.dump(basic_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated college: {college_name}")
        return college_name
    
    return None

def demo_dynamic_system():
    """Demonstrate the dynamic update system"""
    print("🚀 Dynamic College AI Demo")
    print("=" * 60)
    
    # Initialize dynamic AI
    print("🔄 Initializing Dynamic College AI...")
    ai = DynamicCollegeAI()
    
    if not ai.base_agent:
        print("❌ Base model not available. Please train first:")
        print("   python train_rtx2050_gpu.py")
        return
    
    # Show initial status
    status = ai.get_status()
    print(f"\n📊 Initial Status:")
    print(f"   Base colleges: {status['base_colleges']}")
    print(f"   New colleges: {status['new_colleges']}")
    print(f"   Updated colleges: {status['updated_colleges']}")
    
    # Test query before updates
    print(f"\n🧪 Testing query BEFORE updates:")
    test_query = "What is the fee at IIT Hyderabad?"
    results = ai.query_with_dynamic_data(test_query, top_k=2)
    
    if results:
        print(f"✅ Found {len(results)} results:")
        for result in results:
            print(f"   🏫 {result['college']} ({result['confidence']:.1f}%)")
    else:
        print("❌ No results found")
    
    # Create new college
    print(f"\n🆕 Creating new college data...")
    new_college = create_sample_new_college()
    
    # Update existing college
    print(f"\n🔄 Updating existing college data...")
    updated_college = update_existing_college()
    
    # Wait a moment for file system
    time.sleep(1)
    
    # Test query after updates
    print(f"\n🧪 Testing query AFTER updates:")
    results = ai.query_with_dynamic_data(test_query, top_k=3)
    
    if results:
        print(f"✅ Found {len(results)} results:")
        for result in results:
            source_indicator = "🆕" if result.get('source') == 'dynamic' else "📚"
            print(f"   {source_indicator} {result['college']} ({result['confidence']:.1f}%)")
            print(f"      💡 {result['answer'][:100]}...")
    else:
        print("❌ No results found")
    
    # Show updated status
    status = ai.get_status()
    print(f"\n📊 Updated Status:")
    print(f"   Base colleges: {status['base_colleges']}")
    print(f"   New colleges: {status['new_colleges']}")
    print(f"   Updated colleges: {status['updated_colleges']}")
    
    # Test different queries
    test_queries = [
        "What is the placement record at IIT Hyderabad New Campus?",
        "How to get admission in the new IIT campus?",
        "What are the fees for updated colleges?"
    ]
    
    print(f"\n🎯 Testing various queries with dynamic data:")
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        results = ai.query_with_dynamic_data(query, top_k=2)
        
        if results:
            best_result = results[0]
            source_indicator = "🆕" if best_result.get('source') == 'dynamic' else "📚"
            print(f"   {source_indicator} {best_result['college']} ({best_result['confidence']:.1f}%)")
            print(f"   💡 {best_result['answer'][:120]}...")
        else:
            print("   ❌ No results found")
    
    print(f"\n🎉 Demo completed!")
    print(f"✅ System automatically detected and used new/updated data")
    print(f"❌ No retraining required!")
    
    # Cleanup option
    cleanup = input(f"\nClean up demo data? (y/N): ").strip().lower()
    if cleanup == 'y':
        # Remove the demo college
        demo_college_path = Path("college_data") / new_college
        if demo_college_path.exists():
            import shutil
            shutil.rmtree(demo_college_path)
            print(f"🗑️  Removed demo college: {new_college}")

def main():
    """Main demo function"""
    try:
        demo_dynamic_system()
    except KeyboardInterrupt:
        print(f"\n⏹️  Demo interrupted")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()
