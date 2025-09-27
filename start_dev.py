#!/usr/bin/env python3
"""
Development mode - starts app with dog detection disabled for testing
"""

import os
import sys

def main():
    print("🐕 Development Mode - Dog detection disabled")
    print("📝 You can upload any image for testing")
    
    # Set development environment
    os.environ['FLASK_ENV'] = 'development'
    os.environ['SKIP_DOG_CHECK'] = 'true'
    
    # Import and run the app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
