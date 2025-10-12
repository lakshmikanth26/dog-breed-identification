#!/usr/bin/env python3
"""
Development mode - starts app with dog detection disabled for testing
Automatically uses correct Python version from venv_teachable
"""

import os
import sys
import subprocess
import platform

def main():
    # Check if running from correct venv
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Not in a virtual environment, activate and restart
        print("\n" + "="*60)
        print("🔄 Activating virtual environment...")
        print("="*60 + "\n")
        
        # Determine venv python path
        if platform.system() == "Windows":
            venv_python = "venv_teachable\\Scripts\\python.exe"
        else:
            venv_python = "venv_teachable/bin/python"
        
        # Check if venv exists
        if not os.path.exists(venv_python):
            print("❌ Virtual environment not found!")
            print("   Please run: python setup.py")
            sys.exit(1)
        
        # Restart script with venv python
        print(f"✅ Using: {venv_python}\n")
        subprocess.run([venv_python, __file__] + sys.argv[1:])
        sys.exit(0)
    
    # We're in the venv, proceed
    print("\n" + "="*60)
    print("🐕 Dog Breed Identification - Development Mode")
    print("="*60 + "\n")
    
    print(f"✅ Python: {sys.version.split()[0]}")
    print(f"✅ Virtual env: {sys.prefix}")
    
    # Set development environment
    os.environ['FLASK_ENV'] = 'development'
    os.environ['SKIP_DOG_CHECK'] = 'true'
    os.environ['PORT'] = '5001'
    
    print("✅ Dog detection: DISABLED")
    print("✅ Debug mode: ON")
    print("✅ Port: 5001")
    print("\n⏹️  Press Ctrl+C to stop\n")
    
    # Import and run the app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == "__main__":
    main()
