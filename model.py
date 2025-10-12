"""
Dog Breed Identification Model using Keras
"""

import logging
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and labels
_model = None
_labels = None

# Model configuration
MODEL_PATH = 'model/keras_model.h5'  # Updated to match your model filename
LABELS_PATH = 'model/labels.txt'
IMG_SIZE = (224, 224)  # Standard size for most CNN models




def load_model():
    """
    Load the Keras model and labels
    """
    global _model, _labels
    
    if _model is not None and _labels is not None:
        return _model, _labels
    
    try:
        # Load the trained model
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please add your trained model.")
        
        logger.info(f"Loading trained model from {MODEL_PATH}")
        
        # Load model with custom objects to handle 'groups' parameter
        import tensorflow as tf
        
        # Create a custom DepthwiseConv2D class that ignores 'groups'
        class CompatibleDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
            @classmethod
            def from_config(cls, config):
                # Remove 'groups' parameter if present
                config = config.copy()
                config.pop('groups', None)
                # Call parent's from_config with cleaned config
                return super(CompatibleDepthwiseConv2D, cls).from_config(config)
        
        # Use custom objects when loading
        custom_objects = {'DepthwiseConv2D': CompatibleDepthwiseConv2D}
        
        # Load model with custom objects
        _model = tf.keras.models.load_model(MODEL_PATH, custom_objects=custom_objects, compile=False)
        logger.info("✅ Trained model loaded successfully (with compatibility fix)")
            
        # Load labels
        if not os.path.exists(LABELS_PATH):
            raise FileNotFoundError(f"Labels file not found at {LABELS_PATH}. Please add your labels.txt file.")
        
        logger.info(f"Loading labels from {LABELS_PATH}")
        with open(LABELS_PATH, 'r') as f:
            _labels = []
            for line in f.readlines():
                line = line.strip()
                if line:  # Skip empty lines
                    # Handle format like "0 Golden Retriever" or just "Golden Retriever"
                    if ' ' in line and line.split()[0].isdigit():
                        # Format: "0 Golden Retriever" - skip the index
                        _labels.append(' '.join(line.split()[1:]))
                    else:
                        # Format: "Golden Retriever" - use as is
                        _labels.append(line)
        logger.info(f"✅ Loaded {len(_labels)} breed labels")
        
        logger.info(f"Model ready - Input shape: {_model.input_shape}, Output classes: {len(_labels)}")
        return _model, _labels
        
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        logger.error("Cannot load model! Please check:")
        logger.error(f"  1. Model file exists: {MODEL_PATH}")
        logger.error(f"  2. Labels file exists: {LABELS_PATH}")
        logger.error("  3. TensorFlow version compatibility")
        raise RuntimeError(f"Failed to load model: {e}")


def preprocess_image(image_path):
    """
    Preprocess image for model prediction using OpenCV
    Matches the exact preprocessing used in your training code
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Preprocessed image array ready for prediction
    """
    try:
        import cv2
        
        # Read image using OpenCV
        image = cv2.imread(image_path)
        
        # OpenCV reads as BGR, convert to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize using OpenCV (matches your code exactly)
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        
        # Make numpy array and reshape (matches your code)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        
        # Normalize the image (matches your code exactly)
        # Range: -1 to 1
        image = (image / 127.5) - 1
        
        return image
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise


def predict_breed(image_path):
    """
    Predict dog breed from image
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (breed_name, confidence)
    """
    model, labels = load_model()
    
    # Preprocess image
    img_array = preprocess_image(image_path)
    
    # Make prediction
    predictions = model.predict(img_array, verbose=0)
    
    # Get top prediction
    top_idx = np.argmax(predictions[0])
    top_confidence = float(predictions[0][top_idx])
    top_breed = labels[top_idx]
    
    # Format breed name (replace underscores with spaces)
    top_breed = top_breed.replace('_', ' ').title()
    
    logger.info(f"Prediction: {top_breed} ({top_confidence*100:.2f}%)")
    return top_breed, top_confidence


def get_top_predictions(image_path, top_k=3):
    """
    Get top K breed predictions
    
    Args:
        image_path: Path to the image file
        top_k: Number of top predictions to return
        
    Returns:
        List of tuples (breed_name, confidence) sorted by confidence
    """
    model, labels = load_model()
    
    # Preprocess image
    img_array = preprocess_image(image_path)
    
    # Make prediction
    predictions = model.predict(img_array, verbose=0)[0]
    
    # Get top K predictions (limit to available classes)
    top_k = min(top_k, len(labels))
    top_indices = np.argsort(predictions)[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        breed = labels[idx].replace('_', ' ').title()
        confidence = float(predictions[idx])
        results.append((breed, confidence))
    
    logger.info(f"Top {top_k} predictions: {results}")
    return results


def is_likely_dog(image_path, threshold=0.1):
    """
    Check if image likely contains a dog based on prediction confidence
    
    Args:
        image_path: Path to the image file
        threshold: Minimum confidence threshold
        
    Returns:
        Boolean indicating if image likely contains a dog
    """
    try:
        _, confidence = predict_breed(image_path)
        
        # If we have reasonable confidence, assume it's a dog
        is_dog = confidence >= threshold
        
        logger.info(f"Dog detection: {is_dog} (confidence: {confidence*100:.2f}%)")
        return is_dog
        
    except Exception as e:
        logger.error(f"Error during dog detection: {e}")
        # Default to allowing the image through
        return True
