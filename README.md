# 🐕 Dog Breed Identification App

A clean and simple Flask web application that identifies dog breeds using a Keras deep learning model.

## ✨ Features

- **🤖 Powered by Keras**: Deep learning model for dog breed identification
- **🎯 Simple & Clean**: Minimal codebase, easy to understand
- **📱 Modern UI**: Beautiful, responsive web interface
- **🔍 Smart Detection**: Accurately identifies if image contains a dog
- **📊 Multiple Predictions**: Shows top 3 breed matches with confidence scores
- **📝 Breed Information**: Detailed descriptions for each identified breed

## 🚀 Quick Start

### 1. Setup
```bash
# Clone/download the project
cd dog-breed-identification

# Run setup (creates virtual environment and installs dependencies)
python setup.py
```

### 2. Add Your Trained Model (Optional for Development)
Place your trained Keras model in the `model/` directory:
- `model/dog_breed_model.h5` - Your trained Keras model
- `model/labels.txt` - Breed labels (one per line)

**Note**: For development/testing, the app will use a dummy model if no trained model is present.

### 3. Start the App
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Start the app
python app.py

# OR development mode (allows any images for testing)
python start_dev.py
```

### 4. Use the App
1. Open: http://localhost:5000
2. Upload a dog image
3. Get accurate breed identification!

## 📁 Project Structure

```
dog-breed-identification/
├── app.py              # Main Flask application
├── model.py           # Keras model wrapper  
├── model/             # Model files directory
│   ├── dog_breed_model.h5  # Your trained model (add this)
│   ├── labels.txt          # Breed labels (add this)
│   └── README.md           # Model setup instructions
├── breed_info.json   # Breed descriptions database
├── requirements.txt  # Dependencies
├── setup.py         # Setup script
├── start_dev.py     # Development mode
├── env.example      # Environment variables template
├── .env            # Your environment variables (created by setup)
├── static/css/     # Styling
├── templates/      # HTML templates
└── uploads/       # Temporary uploads
```

## 🔧 Dependencies

**Core dependencies:**
- Flask (web framework)
- Pillow (image processing)
- TensorFlow/Keras (deep learning)
- NumPy (numerical processing)
- Gunicorn (production server)

## 💡 How It Works

1. **Upload**: User uploads dog image via web interface
2. **Preprocessing**: Image is resized and normalized for the model
3. **Prediction**: Keras model identifies the breed
4. **Results**: App displays breed name, confidence, and description
5. **Development**: Uses dummy model if trained model not present

## 🎯 Benefits

### Why Keras?
- **🎯 Customizable**: Train on your own dataset for specific needs
- **🚀 Fast Inference**: Local predictions with no API calls
- **💾 Offline Capable**: Works without internet connection
- **🔒 Privacy**: Images never leave your server
- **💰 No API Costs**: Completely free to run

## 🛠️ Configuration

### Environment Variables
```bash
FLASK_ENV=development               # Optional: development mode
SKIP_DOG_CHECK=true                # Optional: disable dog detection
PORT=5000                          # Optional: custom port
SECRET_KEY=your_secret_key         # Optional: custom secret key
```

### Development Mode
```bash
# Start with dog detection disabled (for testing any images)
python start_dev.py
```

### Adding Your Trained Model

1. Train your Keras model with dog breed dataset
2. Save model as `model/dog_breed_model.h5`
3. Create `model/labels.txt` with breed names (one per line)
4. Restart the app

See `model/README.md` for detailed instructions.

## 🔒 Security

- API keys stored in environment variables
- Temporary file cleanup
- Input validation and sanitization
- No sensitive data stored

## 📊 API Usage

The app also provides a JSON API:

```bash
# Upload image for prediction
curl -X POST -F "file=@dog.jpg" http://localhost:5000/api/predict

# Response
{
  "success": true,
  "top_prediction": {
    "breed": "Golden Retriever",
    "confidence": 92.5
  },
  "all_predictions": [...],
  "breed_info": {...}
}
```

## 🚀 Deployment

Ready for deployment on:
- **Heroku**: `git push heroku main`
- **Render**: Connect GitHub repo
- **Railway**: One-click deploy
- **Vercel**: Serverless deployment
- **Google Cloud**: App Engine ready

## 💰 Costs

**Completely Free:**
- No API costs
- No usage limits
- Only hosting costs if deploying to cloud

## 🆘 Troubleshooting

### Common Issues

**"Model file not found"**
- Using dummy model for development
- Add your trained model to `model/` directory
- See `model/README.md` for instructions

**"TensorFlow not installed"**
```bash
pip install -r requirements.txt
```

**Port already in use**
- App automatically finds free port
- Or set custom port: `export PORT=8000`

### Getting Help
1. Check logs in terminal
2. Verify dependencies are installed
3. Check model files in `model/` directory

## 🎉 That's It!

You now have a professional dog breed identification app powered by Keras deep learning! 🐕✨

---

**Made with ❤️ using TensorFlow/Keras**