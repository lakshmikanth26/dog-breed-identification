#!/usr/bin/env python3
"""
Simple setup script for Dog Breed Identification App
"""

import os
import sys
import subprocess
import platform

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

def install_dependencies():
    """Install dependencies"""
    python_exe, pip_exe = get_python_executable()
    
    # Upgrade pip first
    run_command(f'"{pip_exe}" install --upgrade pip', "Upgrading pip")
    
    # Install dependencies
    return run_command(f'"{pip_exe}" install -r requirements.txt', "Installing dependencies")

def create_directories():
    """Create necessary directories"""
    directories = ["static/css", "templates", "uploads"]
    
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
        print("📝 Please edit .env file and add your Gemini API key")
        return True
    elif os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    else:
        print("⚠️  No env.example file found")
        return False

def main():
    """Main setup function"""
    print("🐕 Dog Breed Identification App Setup")
    print("=" * 40)
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher required")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Final instructions
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    
    print("\n📋 Next steps:")
    print("1. Get your Gemini API key:")
    print("   https://aistudio.google.com/app/apikey")
    
    print("\n2. Add your API key to .env file:")
    print("   GEMINI_API_KEY=your_api_key_here")
    
    print("\n3. Start the app:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\python app.py")
    else:
        print("   venv/bin/python app.py")
    
    print("\n4. Open your browser:")
    print("   http://localhost:5000")
    
    print("\n💡 Quick commands:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate     # Activate virtual environment")
        print("   python start_dev.py       # Start in development mode")
    else:
        print("   source venv/bin/activate  # Activate virtual environment") 
        print("   python start_dev.py       # Start in development mode")

if __name__ == "__main__":
    main()