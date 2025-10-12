#!/usr/bin/env python3
"""
Setup script for Dog Breed Identification App
Automatically installs correct Python version and creates virtual environment
"""

import os
import sys
import subprocess
import platform
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def get_python_executable():
    """Get the correct Python executable"""
    if platform.system() == "Windows":
        venv_python = "venv\\Scripts\\python.exe"
        venv_pip = "venv\\Scripts\\pip.exe"
    else:
        venv_python = "venv/bin/python"
        venv_pip = "venv/bin/pip"
    
    if os.path.exists(venv_python):
        return venv_python, venv_pip
    else:
        return sys.executable, "pip"

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def install_dependencies(venv_path):
    """Install dependencies in the virtual environment"""
    # Determine pip path in venv
    if platform.system() == "Windows":
        pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        pip_exe = os.path.join(venv_path, "bin", "pip")
    
    print("\n📦 Installing dependencies...")
    
    # Upgrade pip first
    try:
        subprocess.run([pip_exe, "install", "--upgrade", "pip"], check=True, capture_output=True)
        print("   ✅ Pip upgraded")
    except Exception as e:
        print(f"   ⚠️  Pip upgrade failed: {e}")
    
    # Install dependencies
    try:
        print("   Installing packages (this may take 2-3 minutes)...")
        result = subprocess.run([pip_exe, "install", "-r", "requirements.txt"], 
                              check=True, capture_output=True, text=True)
        print("   ✅ All dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Installation failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["static/css", "templates", "uploads", "model"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment():
    """Setup environment file"""
    if not os.path.exists(".env") and os.path.exists("env.example"):
        print("\n📝 Setting up environment file...")
        
        # Copy example file
        with open("env.example", "r") as f:
            content = f.read()
        
        with open(".env", "w") as f:
            f.write(content)
        
        print("✅ Created .env file from env.example")
        return True
    elif os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    else:
        print("⚠️  No env.example file found")
        return False

def check_python_version():
    """Check if correct Python version is available"""
    # Teachable Machine models require Python 3.9-3.11
    required_versions = ['3.11', '3.10', '3.9']
    
    print("\n🔍 Checking for compatible Python version...")
    print("   Teachable Machine models require Python 3.9, 3.10, or 3.11")
    
    # Check current Python
    current = sys.version_info
    current_version = f"{current.major}.{current.minor}"
    print(f"   Current Python: {current_version}")
    
    if current_version in required_versions:
        print(f"   ✅ Current Python {current_version} is compatible!")
        return sys.executable
    
    # Check for other Python versions
    for version in required_versions:
        python_cmd = f"python{version}"
        python_path = shutil.which(python_cmd)
        if python_path:
            print(f"   ✅ Found Python {version} at: {python_path}")
            return python_path
    
    # No compatible version found
    print("\n   ❌ No compatible Python version found!")
    print("\n   📦 Installing Python 3.11...")
    
    if platform.system() == "Darwin":  # macOS
        print("   Using Homebrew to install Python 3.11...")
        try:
            # Check if Homebrew is installed
            if not shutil.which("brew"):
                print("\n   ❌ Homebrew not found!")
                print("   Please install Homebrew first:")
                print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                sys.exit(1)
            
            # Install Python 3.11
            subprocess.run(["brew", "install", "python@3.11"], check=True)
            python_path = shutil.which("python3.11")
            if python_path:
                print(f"   ✅ Python 3.11 installed successfully!")
                return python_path
        except Exception as e:
            print(f"   ❌ Failed to install Python: {e}")
    
    # If we get here, installation failed
    print("\n   ⚠️  Automatic installation failed!")
    print("\n   Please install Python 3.11 manually:")
    print("   macOS: brew install python@3.11")
    print("   Or download from: https://www.python.org/downloads/")
    sys.exit(1)

def main():
    """Main setup function"""
    print("\n" + "=" * 60)
    print("🐕 Dog Breed Identification App Setup")
    print("   (Teachable Machine Compatible)")
    print("=" * 60)
    
    # Check and get correct Python version
    python_executable = check_python_version()
    
    # Create virtual environment with correct Python version
    venv_path = "venv_teachable"
    print(f"\n📦 Creating virtual environment with Python {python_executable}...")
    try:
        subprocess.run([python_executable, "-m", "venv", venv_path], check=True)
        print(f"   ✅ Virtual environment created: {venv_path}")
    except Exception as e:
        print(f"   ❌ Failed to create virtual environment: {e}")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies in the venv
    if not install_dependencies(venv_path):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Save Python path for start_dev.py
    venv_python = "venv_teachable/bin/python" if platform.system() != "Windows" else "venv_teachable\\Scripts\\python.exe"
    with open(".python_path", "w") as f:
        f.write(venv_python)
    
    # Final instructions
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    
    print("\n📋 Your setup:")
    print(f"   ✓ Python version: {python_executable}")
    print(f"   ✓ Virtual environment: venv_teachable/")
    print(f"   ✓ All dependencies installed")
    print(f"   ✓ Model: model/keras_model.h5")
    
    print("\n🚀 To start the app:")
    print("   python start_dev.py")
    
    print("\n   Or manually:")
    if platform.system() == "Windows":
        print("   venv_teachable\\Scripts\\activate")
    else:
        print("   source venv_teachable/bin/activate")
    print("   python app.py")
    
    print("\n📍 Then open: http://localhost:5001")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()