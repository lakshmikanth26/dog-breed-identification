"""
Flask Web Application for Dog Breed Identification
"""

import os
import json
import logging
import socket
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import uuid
from datetime import datetime

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file if it exists"""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

# Import our model functions
from model import predict_breed, get_top_predictions, is_likely_dog

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'pjpeg', 'jfif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Constants
NO_FILE_SELECTED_MSG = 'No file selected'

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_breed_info():
    """Load breed information from JSON file"""
    try:
        with open('breed_info.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("breed_info.json not found")
        return {}
    except json.JSONDecodeError:
        logger.error("Error parsing breed_info.json")
        return {}

def get_breed_description(breed_name):
    """Get description for a specific breed"""
    breed_info = load_breed_info()
    
    # Try exact match first
    if breed_name in breed_info:
        return breed_info[breed_name]
    
    # Try case-insensitive match
    for breed, info in breed_info.items():
        if breed.lower() == breed_name.lower():
            return info
    
    # Try partial match
    breed_lower = breed_name.lower()
    for breed, info in breed_info.items():
        if breed_lower in breed.lower() or breed.lower() in breed_lower:
            return info
    
    return {
        "description": "A wonderful dog breed with unique characteristics.",
        "temperament": "Friendly and loyal",
        "size": "Varies",
        "origin": "Unknown"
    }

def cleanup_old_files():
    """Clean up old uploaded files to prevent disk space issues"""
    try:
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            return
        
        current_time = datetime.now().timestamp()
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                # Delete files older than 1 hour
                if current_time - os.path.getctime(file_path) > 3600:
                    os.remove(file_path)
                    logger.info(f"Cleaned up old file: {filename}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

@app.route('/')
def index():
    """Home page with upload form"""
    cleanup_old_files()  # Clean up old files on each visit
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            flash(NO_FILE_SELECTED_MSG, 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            flash(NO_FILE_SELECTED_MSG, 'error')
            return redirect(url_for('index'))
        
        # Check file type
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF, BMP, WebP)', 'error')
            return redirect(url_for('index'))
        
        # Generate unique filename to avoid conflicts
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save uploaded file
        file.save(filepath)
        logger.info(f"File saved: {filepath}")
        
        # Check if image likely contains a dog (skip in development mode)
        # Note: Disabled by default for custom models with specific breeds
        skip_dog_check = os.environ.get('SKIP_DOG_CHECK', 'true').lower() == 'true'
        
        print(f"\n{'='*60}")
        print(f"🔍 PREDICTION DEBUG INFO")
        print(f"{'='*60}")
        print(f"File: {filename}")
        print(f"SKIP_DOG_CHECK env: {os.environ.get('SKIP_DOG_CHECK', 'NOT SET')}")
        print(f"skip_dog_check value: {skip_dog_check}")
        print(f"Will perform dog check? {not skip_dog_check}")
        
        if not skip_dog_check:
            print(f"⚠️  Running dog detection check...")
            is_dog = is_likely_dog(filepath, threshold=0.05)
            print(f"Dog detection result: {is_dog}")
            if not is_dog:
                print(f"❌ FAILED dog check - rejecting image")
                os.remove(filepath)  # Clean up
                flash('This image does not appear to contain a dog. Please upload a clear image of a dog.', 'warning')
                return redirect(url_for('index'))
            print(f"✅ PASSED dog check")
        else:
            print(f"✅ Dog check SKIPPED (disabled)")
        
        # Get predictions
        print(f"Getting predictions...")
        top_predictions = get_top_predictions(filepath, top_k=3)
        print(f"Top predictions: {top_predictions}")
        print(f"{'='*60}\n")
        
        # Get the top prediction
        top_breed, top_confidence = top_predictions[0]
        
        # Get breed information
        breed_info = get_breed_description(top_breed)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except OSError:
            pass
        
        # Prepare results
        results = {
            'top_breed': top_breed,
            'top_confidence': round(top_confidence * 100, 2),
            'all_predictions': [(breed, round(conf * 100, 2)) for breed, conf in top_predictions],
            'breed_info': breed_info,
            'filename': filename
        }
        
        return render_template('result.html', **results)
    
    except RequestEntityTooLarge:
        flash('File too large. Please upload an image smaller than 16MB.', 'error')
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        flash('An error occurred while processing your image. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions (JSON response)"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': NO_FILE_SELECTED_MSG}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Check if image likely contains a dog (skip in development mode)
            # Note: Disabled by default for custom models with specific breeds
            skip_dog_check = os.environ.get('SKIP_DOG_CHECK', 'true').lower() == 'true'
            
            if not skip_dog_check and not is_likely_dog(filepath, threshold=0.05):
                return jsonify({'error': 'Image does not appear to contain a dog'}), 400
            
            # Get predictions
            top_predictions = get_top_predictions(filepath, top_k=3)
            top_breed, top_confidence = top_predictions[0]
            
            # Get breed information
            breed_info = get_breed_description(top_breed)
            
            # Prepare response
            response = {
                'success': True,
                'top_prediction': {
                    'breed': top_breed,
                    'confidence': round(top_confidence * 100, 2)
                },
                'all_predictions': [
                    {'breed': breed, 'confidence': round(conf * 100, 2)}
                    for breed, conf in top_predictions
                ],
                'breed_info': breed_info
            }
            
            return jsonify(response)
        
        finally:
            # Clean up file
            try:
                os.remove(filepath)
            except OSError:
                pass
    
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Please upload an image smaller than 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}")
    return render_template('500.html'), 500

def find_free_port(start_port=5000, max_port=5100):
    """Find a free port starting from start_port"""
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No free port found between {start_port} and {max_port}")

def is_port_in_use(port):
    """Check if a port is currently in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return False
    except OSError:
        return True

if __name__ == '__main__':
    # Load Keras model
    print("\n" + "="*60)
    print("🐕 DOG BREED IDENTIFICATION APP")
    print("="*60)
    try:
        from model import load_model
        model, labels = load_model()
        print(f"🤖 Model loaded: {len(labels)} dog breeds")
        print(f"📋 Breeds: {labels}")
        logger.info("Keras model loaded successfully")
    except Exception as e:
        logger.warning(f"Could not load model: {e}")
        print("⚠️  Using dummy model for development")
    
    # Show environment configuration
    print(f"\n🔧 Configuration:")
    print(f"   SKIP_DOG_CHECK: {os.environ.get('SKIP_DOG_CHECK', 'NOT SET (defaults to true)')}")
    print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV', 'NOT SET')}")
    print(f"   PORT: {os.environ.get('PORT', '5001 (default)')}")
    print("="*60 + "\n")
    
    # Determine port to use - fixed to 5001 to avoid conflicts
    preferred_port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Check if preferred port is available
    if is_port_in_use(preferred_port):
        logger.warning(f"Port {preferred_port} is busy, finding alternative port...")
        try:
            port = find_free_port(preferred_port + 1)
            logger.info(f"Using alternative port: {port}")
        except RuntimeError as e:
            logger.error(f"Could not find free port: {e}")
            logger.info("Trying to use the preferred port anyway...")
            port = preferred_port
    else:
        port = preferred_port
        logger.info(f"Using port: {port}")
    
    # Run the app
    try:
        print("\n🚀 Starting Dog Breed Identification App")
        print(f"📍 Server running on: http://localhost:{port}")
        print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
        print("⏹️  Press Ctrl+C to stop the server\n")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(f"Port {port} is still busy. Trying to find another port...")
            try:
                alternative_port = find_free_port(port + 1)
                logger.info(f"Found alternative port: {alternative_port}")
                print("\n🚀 Starting Dog Breed Identification App")
                print(f"📍 Server running on: http://localhost:{alternative_port}")
                print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
                print("⏹️  Press Ctrl+C to stop the server\n")
                app.run(host='0.0.0.0', port=alternative_port, debug=debug)
            except RuntimeError:
                logger.error("Could not find any free port. Please check your system.")
                print("❌ Error: Could not start server - no free ports available")
        else:
            logger.error(f"Failed to start server: {e}")
            print(f"❌ Error starting server: {e}")
