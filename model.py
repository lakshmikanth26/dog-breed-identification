"""
Dog Breed Identification Model
Simple and clean implementation using only Gemini AI
"""

import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model():
    """Load model - just a placeholder since we use Gemini AI directly"""
    logger.info("Using Gemini AI for dog breed identification")
    return "gemini"

def predict_breed(image_path):
    """Predict dog breed using free AI APIs"""
    try:
        from free_ai_model import predict_breed_free_ai
        return predict_breed_free_ai(image_path)
    except Exception as e:
        logger.error(f"Free AI prediction failed: {e}")
        # Simple fallback - return a generic response
        return "Mixed Breed Dog", 0.5

def get_top_predictions(image_path, top_k=3):
    """Get top K breed predictions using free AI APIs"""
    try:
        from free_ai_model import get_top_predictions_free_ai
        return get_top_predictions_free_ai(image_path, top_k)
    except Exception as e:
        logger.error(f"Free AI top predictions failed: {e}")
        # Simple fallback
        breed, confidence = predict_breed(image_path)
        return [(breed, confidence)]

def is_likely_dog(image_path, threshold=0.1):
    """Check if image contains a dog using free AI APIs"""
    try:
        from free_ai_model import is_likely_dog_free_ai
        return is_likely_dog_free_ai(image_path, threshold)
    except Exception as e:
        logger.error(f"Free AI dog detection failed: {e}")
        # Fallback - allow all images through
        return True