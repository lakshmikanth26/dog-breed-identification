# 🤖 Gemini AI Integration for Dog Breed Identification

This guide will help you set up Google's Gemini AI for highly accurate dog breed identification.

## ✨ Why Use Gemini AI?

- **🎯 Much Higher Accuracy**: Gemini can identify dog breeds with professional-level accuracy
- **🔍 Better Dog Detection**: Accurately determines if an image contains a dog
- **📝 Detailed Analysis**: Provides reasoning for breed identification
- **🌐 No Training Required**: Uses Google's pre-trained vision models
- **🚀 Easy Setup**: Just need an API key

## 🔧 Setup Instructions

### Step 1: Get Your Gemini API Key

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy the generated API key** (keep it secure!)

### Step 2: Install Dependencies

```bash
# Install Gemini dependencies
python setup_gemini.py

# Or manually:
pip install google-generativeai>=0.3.0
```

### Step 3: Set Your API Key

Choose one of these methods:

#### Option A: Environment Variable (Recommended)

**On macOS/Linux:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**On Windows:**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

#### Option B: Create .env File

Create a `.env` file in the project directory:
```
GEMINI_API_KEY=your_api_key_here
```

#### Option C: Set During Setup

Run the setup script and enter your key when prompted:
```bash
python setup_gemini.py
```

### Step 4: Test the Integration

```bash
# Test Gemini API connection
python test_gemini.py

# Or test with the Flask app
python start_dev.py
```

## 🚀 Usage

Once set up, the Flask app will automatically use Gemini AI for predictions:

1. **Start the app**: `python start_dev.py`
2. **Upload dog images** - Gemini will provide accurate breed identification
3. **Get detailed results** with confidence scores and reasoning

## 📊 Model Hierarchy

The app uses models in this priority order:

1. **🥇 Gemini AI** (Primary - Most Accurate)
   - Uses Google's advanced vision models
   - Provides detailed breed analysis
   - Best accuracy for all dog breeds

2. **🥈 Enhanced Pre-trained Model** (Fallback)
   - Uses ResNet50 with ImageNet weights
   - Good for common breeds
   - Works offline

3. **🥉 Basic TensorFlow Model** (Final Fallback)
   - Simple model architecture
   - Basic breed classification
   - Always available

## 💡 Features with Gemini AI

### Accurate Breed Identification
```python
# Example response
{
    "breed": "Golden Retriever",
    "confidence": 92,
    "reasoning": "Large, golden-colored coat, friendly expression, typical retriever build"
}
```

### Multiple Breed Predictions
```python
# Top 3 predictions
[
    ("Golden Retriever", 0.92),
    ("Labrador Retriever", 0.06),
    ("Nova Scotia Duck Tolling Retriever", 0.02)
]
```

### Smart Dog Detection
- Accurately identifies if an image contains a dog
- Rejects non-dog images with clear explanations
- Handles edge cases (puppies, mixed breeds, etc.)

## 🔒 API Key Security

**Important Security Notes:**

- ✅ **DO**: Store API key in environment variables
- ✅ **DO**: Use .env files (add to .gitignore)
- ✅ **DO**: Rotate keys periodically
- ❌ **DON'T**: Commit API keys to version control
- ❌ **DON'T**: Share API keys publicly
- ❌ **DON'T**: Hardcode keys in source code

## 💰 API Costs

Gemini AI has generous free tiers:

- **Free Tier**: 15 requests per minute, 1,500 requests per day
- **Paid Tier**: Higher limits, very affordable pricing
- **Cost per request**: Typically $0.00025 - $0.001 per image

For most applications, the free tier is sufficient.

## 🛠️ Troubleshooting

### Common Issues

**1. "API key not found" error**
```bash
# Check if key is set
echo $GEMINI_API_KEY  # macOS/Linux
echo %GEMINI_API_KEY%  # Windows

# Set the key
export GEMINI_API_KEY="your_key_here"
```

**2. "google-generativeai not installed"**
```bash
pip install google-generativeai
```

**3. "API quota exceeded"**
- Wait for quota reset (daily/monthly)
- Upgrade to paid tier
- Use fallback models

**4. "Invalid API key"**
- Check key is correct
- Ensure no extra spaces
- Generate new key if needed

### Testing Commands

```bash
# Test API connection
python -c "from gemini_model import test_gemini_api; print(test_gemini_api())"

# Test with sample image
python test_gemini.py

# Check model availability
python -c "from app import *"  # Will show available models
```

## 🎯 Expected Results

With Gemini AI, you should see:

- **90%+ accuracy** for common dog breeds
- **Detailed breed information** and reasoning
- **Proper rejection** of non-dog images
- **Fast response times** (1-3 seconds per image)
- **Consistent results** across different image qualities

## 🔄 Fallback Behavior

If Gemini AI fails (network issues, quota exceeded, etc.), the app automatically falls back to:

1. Enhanced pre-trained model (still good accuracy)
2. Basic TensorFlow model (basic functionality)

This ensures your app always works, even without Gemini AI.

## 📞 Support

If you encounter issues:

1. **Check the logs** - Flask app shows detailed error messages
2. **Test API key** - Use `python test_gemini.py`
3. **Verify setup** - Run `python setup_gemini.py` again
4. **Check quotas** - Visit Google AI Studio dashboard

---

🎉 **That's it!** Your Flask app now has professional-grade dog breed identification powered by Google's Gemini AI!
