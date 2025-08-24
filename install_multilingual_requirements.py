#!/usr/bin/env python3
"""
Install requirements for Multilingual College AI Agent
Installs all necessary packages for multilingual support
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package_name}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f"   ✅ {package_name} installed successfully")
            return True
        else:
            print(f"   ❌ Failed to install {package_name}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install {package_name}")
        print(f"   Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error installing {package_name}: {e}")
        return False

def main():
    print("🌐 Installing Multilingual College AI Agent Requirements")
    print("=" * 70)
    
    # Core ML and AI packages
    core_packages = [
        "torch>=1.9.0",
        "transformers>=4.20.0",
        "sentence-transformers>=2.2.0",
        "scikit-learn>=1.0.0",
        "faiss-cpu>=1.7.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "flask>=2.0.0"
    ]
    
    # Translation and language processing packages
    translation_packages = [
        "googletrans==4.0.0-rc1",
        "langdetect>=1.0.9",
        "requests>=2.25.0"
    ]
    
    # Optional packages for enhanced functionality
    optional_packages = [
        "jupyter>=1.0.0",
        "ipywidgets>=7.6.0",
        "tqdm>=4.62.0"
    ]
    
    all_packages = core_packages + translation_packages + optional_packages
    
    print(f"🔧 Installing {len(all_packages)} packages...")
    print("\n📋 Package List:")
    for i, package in enumerate(all_packages, 1):
        print(f"   {i:2d}. {package}")
    
    print(f"\n🚀 Starting installation...")
    
    success_count = 0
    failed_packages = []
    
    # Install core packages first
    print(f"\n📦 Installing Core ML Packages ({len(core_packages)} packages):")
    for i, package in enumerate(core_packages, 1):
        print(f"\n[{i}/{len(core_packages)}] {package}")
        
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    # Install translation packages
    print(f"\n🌐 Installing Translation Packages ({len(translation_packages)} packages):")
    for i, package in enumerate(translation_packages, 1):
        print(f"\n[{i}/{len(translation_packages)}] {package}")
        
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    # Install optional packages
    print(f"\n🔧 Installing Optional Packages ({len(optional_packages)} packages):")
    for i, package in enumerate(optional_packages, 1):
        print(f"\n[{i}/{len(optional_packages)}] {package}")
        
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    # Summary
    print(f"\n" + "=" * 70)
    print(f"📊 Installation Summary:")
    print(f"   ✅ Successfully installed: {success_count}/{len(all_packages)} packages")
    print(f"   ❌ Failed installations: {len(failed_packages)} packages")
    
    if failed_packages:
        print(f"\n⚠️  Failed Packages:")
        for package in failed_packages:
            print(f"   - {package}")
        print(f"\n💡 Try installing failed packages manually:")
        print(f"   pip install {' '.join(failed_packages)}")
    
    if success_count >= len(core_packages) + len(translation_packages):
        print(f"\n🎉 Multilingual College AI Agent is ready!")
        print(f"✅ All essential packages installed successfully")
        print(f"\n🚀 You can now run:")
        print(f"   python train_college_ai_agent.py")
    else:
        print(f"\n⚠️  Some essential packages failed to install")
        print(f"❌ Please resolve installation issues before proceeding")
    
    print(f"\n🌐 Supported Languages:")
    languages = [
        "🇮🇳 Hindi (हिन्दी)",
        "🇮🇳 Bengali (বাংলা)", 
        "🇮🇳 Telugu (తెలుగు)",
        "🇮🇳 Marathi (मराठी)",
        "🇮🇳 Tamil (தமிழ்)",
        "🇮🇳 Gujarati (ગુજરાતી)",
        "🇮🇳 Urdu (اردو)",
        "🇮🇳 Kannada (ಕನ್ನಡ)",
        "🇮🇳 Malayalam (മലയാളം)",
        "🇮🇳 Odia (ଓଡ଼ିଆ)",
        "🇮🇳 Punjabi (ਪੰਜਾਬੀ)",
        "🇮🇳 Assamese (অসমীয়া)",
        "🇮🇳 English"
    ]
    
    for lang in languages:
        print(f"   {lang}")

if __name__ == "__main__":
    main()
