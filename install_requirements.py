"""
Install Requirements for College AI Agent
Automated installation of all required packages
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("📦 Installing Requirements for College AI Agent")
    print("=" * 60)
    
    # Required packages
    packages = [
        "torch",
        "transformers",
        "sentence-transformers", 
        "scikit-learn",
        "faiss-cpu",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "flask"
    ]
    
    print(f"🔧 Installing {len(packages)} packages...")
    
    success_count = 0
    failed_packages = []
    
    for i, package in enumerate(packages, 1):
        print(f"\n📦 [{i}/{len(packages)}] Installing {package}...")
        
        if install_package(package):
            print(f"   ✅ {package} installed successfully")
            success_count += 1
        else:
            print(f"   ❌ Failed to install {package}")
            failed_packages.append(package)
    
    print(f"\n🎉 Installation Summary:")
    print(f"   ✅ Successfully installed: {success_count}/{len(packages)} packages")
    
    if failed_packages:
        print(f"   ❌ Failed packages: {', '.join(failed_packages)}")
        print(f"\n💡 Try installing failed packages manually:")
        for package in failed_packages:
            print(f"   pip install {package}")
    else:
        print(f"   🚀 All packages installed successfully!")
        print(f"\n✅ You can now run: python train_college_ai_agent.py")

if __name__ == "__main__":
    main()
