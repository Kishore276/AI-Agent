#!/usr/bin/env python3
"""
Comprehensive System Health Check
Test all components and identify any remaining issues
"""

import os
import json
import pickle
import traceback
from pathlib import Path

def test_data_integrity():
    """Test college data integrity"""
    print("🔍 Testing College Data Integrity...")
    
    college_data_dir = Path("college_data")
    if not college_data_dir.exists():
        print("❌ College data directory missing")
        return False
    
    expected_files = [
        'basic_info.json', 'courses.json', 'fees_structure.json',
        'admission_process.json', 'facilities.json', 'placements.json', 'faq.json'
    ]
    
    total_colleges = 0
    issues = []
    
    for college_dir in college_data_dir.iterdir():
        if college_dir.is_dir():
            total_colleges += 1
            
            # Check file count
            json_files = list(college_dir.glob("*.json"))
            if len(json_files) != 7:
                issues.append(f"{college_dir.name}: {len(json_files)} files")
                continue
                
            # Check file names
            file_names = [f.name for f in json_files]
            missing = [f for f in expected_files if f not in file_names]
            if missing:
                issues.append(f"{college_dir.name}: Missing {missing}")
                
            # Test JSON validity
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if not data:  # Empty JSON
                            issues.append(f"{college_dir.name}/{json_file.name}: Empty")
                except Exception as e:
                    issues.append(f"{college_dir.name}/{json_file.name}: {e}")
    
    if issues:
        print(f"❌ Found {len(issues)} data issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more issues")
        return False
    else:
        print(f"✅ All {total_colleges} colleges have valid data structure")
        return True

def test_model_files():
    """Test AI model files"""
    print("\n🤖 Testing AI Model Files...")
    
    models_to_test = [
        ("college_ai_agent.pkl", "Primary AI model"),
        ("college_ai_multilingual_ready.pkl", "Multilingual AI model")
    ]
    
    all_good = True
    
    for model_path, description in models_to_test:
        print(f"🔍 Testing {description}...")
        
        if not os.path.exists(model_path):
            print(f"❌ {model_path} missing")
            all_good = False
            continue
            
        try:
            # Test loading
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            # Check essential components
            required_keys = ['qa_pairs', 'colleges_data']
            missing_keys = [key for key in required_keys if key not in model_data]
            
            if missing_keys:
                print(f"❌ {model_path}: Missing keys {missing_keys}")
                all_good = False
                continue
            
            qa_count = len(model_data['qa_pairs'])
            college_count = len(model_data['colleges_data'])
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            
            print(f"✅ {description}: {qa_count} Q&A pairs, {college_count} colleges, {size_mb:.1f} MB")
            
        except Exception as e:
            print(f"❌ Error loading {model_path}: {e}")
            all_good = False
    
    return all_good

def test_agent_functionality():
    """Test AI agent basic functionality"""
    print("\n🧠 Testing AI Agent Functionality...")
    
    try:
        from train_college_ai_agent import CollegeAIAgent
        
        # Test English-only agent
        print("🔍 Testing English-only agent...")
        agent = CollegeAIAgent(enable_multilingual=False)
        
        if len(agent.colleges_data) == 0:
            print("❌ No college data loaded")
            return False
            
        if len(agent.qa_pairs) == 0:
            print("❌ No Q&A pairs generated")
            return False
        
        print(f"✅ Agent loaded: {len(agent.colleges_data)} colleges, {len(agent.qa_pairs)} Q&A pairs")
        
        # Test a simple query
        if hasattr(agent, 'query_agent'):
            try:
                results = agent.query_agent("What is the fee at IIT Bombay?", top_k=3)
                if results and len(results) > 0:
                    print(f"✅ Query test successful: {len(results)} results returned")
                else:
                    print("⚠️ Query returned no results")
            except Exception as e:
                print(f"⚠️ Query test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_imports():
    """Test critical imports"""
    print("\n📦 Testing Critical Imports...")
    
    imports_to_test = [
        ("train_college_ai_agent", "Main agent module"),
        ("sentence_transformers", "Sentence transformers"),
        ("faiss", "FAISS vector search"),
        ("torch", "PyTorch"),
        ("transformers", "Hugging Face transformers"),
        ("googletrans", "Google Translate"),
        ("flask", "Flask web framework")
    ]
    
    all_good = True
    
    for module, description in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError as e:
            print(f"❌ {description}: {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️ {description}: {e}")
    
    return all_good

def test_deployment_files():
    """Test deployment package"""
    print("\n🚀 Testing Deployment Files...")
    
    deployment_dir = Path("college_ai_deployment")
    if not deployment_dir.exists():
        print("❌ Deployment directory missing")
        return False
    
    expected_files = [
        "api_server.py",
        "query_agent.py",
        "README.md"
    ]
    
    issues = []
    for file_name in expected_files:
        file_path = deployment_dir / file_name
        if not file_path.exists():
            issues.append(f"Missing: {file_name}")
        else:
            # Test Python files for syntax
            if file_name.endswith('.py'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        compile(f.read(), str(file_path), 'exec')
                except SyntaxError as e:
                    issues.append(f"Syntax error in {file_name}: {e}")
    
    if issues:
        print("❌ Deployment issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Deployment package is complete")
        return True

def generate_health_report():
    """Generate comprehensive health report"""
    print("\n" + "="*60)
    print("🏥 COMPREHENSIVE SYSTEM HEALTH REPORT")
    print("="*60)
    
    tests = [
        ("Data Integrity", test_data_integrity),
        ("Model Files", test_model_files),
        ("Agent Functionality", test_agent_functionality),
        ("Critical Imports", test_imports),
        ("Deployment Files", test_deployment_files)
    ]
    
    results = {}
    overall_health = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            if not result:
                overall_health = False
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
            overall_health = False
    
    print("\n📊 SUMMARY:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n🎯 OVERALL HEALTH: {'✅ EXCELLENT' if overall_health else '⚠️ ISSUES FOUND'}")
    
    if overall_health:
        print("\n🎉 All systems operational! Your AI agent is ready for use.")
    else:
        print("\n🔧 Some issues found. Please review the failures above.")
    
    return overall_health

if __name__ == "__main__":
    generate_health_report()
