"""
Gemini AI Dog Breed Identification Model
Uses Google's Gemini API for accurate dog breed identification
"""

import os
import logging
import json
import base64
from PIL import Image
import requests
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google GenerativeAI not available. Install with: pip install google-generativeai")

class GeminiDogBreedClassifier:
    """Dog breed classifier using Google Gemini API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.model = None
        
        if not self.api_key:
            logger.error("Gemini API key not found. Set GEMINI_API_KEY environment variable or pass api_key parameter")
            raise ValueError("Gemini API key required")
        
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package not installed")
        
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize Gemini model"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise
    
    def prepare_image(self, image_path):
        """Prepare image for Gemini API"""
        try:
            # Open and convert image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (Gemini has size limits)
            max_size = 1024
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            return image
        
        except Exception as e:
            logger.error(f"Error preparing image: {e}")
            raise
    
    def predict_breed(self, image_path):
        """Predict dog breed using Gemini"""
        try:
            image = self.prepare_image(image_path)
            
            prompt = """
            Analyze this image and identify the dog breed. Please provide:
            1. The most likely dog breed name
            2. Your confidence level as a percentage (0-100)
            3. If you're not sure it's a dog, say so
            
            Format your response as JSON like this:
            {
                "breed": "Golden Retriever",
                "confidence": 85,
                "is_dog": true,
                "reasoning": "Brief explanation of why you think it's this breed"
            }
            
            If it's not a dog or you can't identify the breed, set "is_dog" to false and "breed" to "Unknown".
            """
            
            response = self.model.generate_content([prompt, image])
            
            # Parse the response
            response_text = response.text.strip()
            
            # Try to extract JSON from the response
            try:
                # Remove markdown code blocks if present
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0]
                
                result = json.loads(response_text)
                
                breed = result.get('breed', 'Unknown')
                confidence = result.get('confidence', 0) / 100.0  # Convert to 0-1 range
                is_dog = result.get('is_dog', True)
                
                if not is_dog:
                    return "Not a dog", 0.0
                
                return breed, confidence
                
            except json.JSONDecodeError:
                # Fallback: try to parse the response manually
                logger.warning("Could not parse JSON response, attempting manual parsing")
                return self.parse_text_response(response_text)
        
        except Exception as e:
            logger.error(f"Error in Gemini prediction: {e}")
            return "Error", 0.0
    
    def parse_text_response(self, text):
        """Fallback method to parse text response"""
        try:
            # Look for breed name and confidence in the text
            lines = text.lower().split('\n')
            breed = "Unknown"
            confidence = 0.1
            
            for line in lines:
                if 'breed' in line and ':' in line:
                    breed = line.split(':')[1].strip().title()
                elif 'confidence' in line and any(char.isdigit() for char in line):
                    # Extract percentage
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        confidence = int(numbers[0]) / 100.0
            
            return breed, confidence
        
        except Exception as e:
            logger.error(f"Error parsing text response: {e}")
            return "Unknown", 0.1
    
    def get_top_predictions(self, image_path, top_k=3):
        """Get top K predictions from Gemini"""
        try:
            image = self.prepare_image(image_path)
            
            prompt = f"""
            Analyze this image and identify the dog breed. Please provide the top {top_k} most likely dog breeds with confidence scores.
            
            Format your response as JSON like this:
            {{
                "is_dog": true,
                "predictions": [
                    {{"breed": "Golden Retriever", "confidence": 85}},
                    {{"breed": "Labrador Retriever", "confidence": 12}},
                    {{"breed": "Nova Scotia Duck Tolling Retriever", "confidence": 3}}
                ]
            }}
            
            If it's not a dog, set "is_dog" to false and return empty predictions.
            Make sure confidence scores are percentages (0-100) and sum to approximately 100.
            """
            
            response = self.model.generate_content([prompt, image])
            response_text = response.text.strip()
            
            # Parse JSON response
            try:
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0]
                
                result = json.loads(response_text)
                
                if not result.get('is_dog', True):
                    return [("Not a dog", 0.0)]
                
                predictions = []
                for pred in result.get('predictions', []):
                    breed = pred.get('breed', 'Unknown')
                    confidence = pred.get('confidence', 0) / 100.0
                    predictions.append((breed, confidence))
                
                return predictions[:top_k]
            
            except json.JSONDecodeError:
                # Fallback to single prediction
                breed, confidence = self.predict_breed(image_path)
                return [(breed, confidence)]
        
        except Exception as e:
            logger.error(f"Error getting top predictions: {e}")
            return [("Error", 0.0)]
    
    def is_likely_dog(self, image_path, threshold=0.1):
        """Check if image contains a dog"""
        try:
            image = self.prepare_image(image_path)
            
            prompt = """
            Look at this image and determine if it contains a dog. 
            Respond with just "YES" if it's a dog, or "NO" if it's not a dog.
            Be strict - only say YES if you're confident it's actually a dog.
            """
            
            response = self.model.generate_content([prompt, image])
            response_text = response.text.strip().upper()
            
            return "YES" in response_text
        
        except Exception as e:
            logger.error(f"Error in dog detection: {e}")
            return True  # Default to allowing the image

# Global instance
gemini_classifier = None

def get_gemini_classifier():
    """Get global Gemini classifier instance"""
    global gemini_classifier
    if gemini_classifier is None:
        try:
            gemini_classifier = GeminiDogBreedClassifier()
        except Exception as e:
            logger.error(f"Failed to initialize Gemini classifier: {e}")
            raise
    return gemini_classifier

def predict_breed_gemini(image_path):
    """Predict breed using Gemini"""
    classifier = get_gemini_classifier()
    return classifier.predict_breed(image_path)

def get_top_predictions_gemini(image_path, top_k=3):
    """Get top predictions using Gemini"""
    classifier = get_gemini_classifier()
    return classifier.get_top_predictions(image_path, top_k)

def is_likely_dog_gemini(image_path, threshold=0.1):
    """Check if image is a dog using Gemini"""
    classifier = get_gemini_classifier()
    return classifier.is_likely_dog(image_path, threshold)

# Test function
def test_gemini_api():
    """Test if Gemini API is working"""
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return False, "GEMINI_API_KEY environment variable not set"
        
        if not GEMINI_AVAILABLE:
            return False, "google-generativeai package not installed"
        
        # Try to initialize
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with a simple prompt
        response = model.generate_content("Say 'API working' if you can read this.")
        
        if "API working" in response.text:
            return True, "Gemini API is working"
        else:
            return False, "Unexpected API response"
    
    except Exception as e:
        return False, f"API test failed: {e}"
