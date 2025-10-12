# Dog Breed Model Files

This directory contains the Keras model files for dog breed identification.

## Required Files

1. **dog_breed_model.h5** - Your trained Keras model file
2. **labels.txt** - Text file with breed labels (one per line)

## How to Add Your Trained Model

### 1. Save your trained model

```python
# After training your model
model.save('model/dog_breed_model.h5')
```

### 2. Create labels.txt

Create a text file with one breed label per line, matching the order of your model's output classes:

```text
Chihuahua
Japanese_spaniel
Maltese_dog
Pekinese
...
```

### 3. Place files in this directory

```
model/
├── dog_breed_model.h5    # Your trained model
├── labels.txt            # Breed labels
└── README.md             # This file
```

## Model Requirements

- **Input shape**: (224, 224, 3) - RGB images
- **Output**: Softmax probabilities for each breed class
- **Format**: Keras .h5 format

## Development Mode

Until you add your trained model, the app will use a dummy model for testing. The dummy model creates random predictions for demonstration purposes.

## Example Training Code

```python
import tensorflow as tf
from tensorflow import keras

# Define your model
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(128, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(num_breeds, activation='softmax')
])

# Compile and train
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train your model...
# model.fit(...)

# Save the model
model.save('model/dog_breed_model.h5')
```

## Notes

- The app automatically detects and loads your model when present
- Image preprocessing is handled automatically (resize to 224x224, normalize to 0-1)
- Supports standard Keras model formats (.h5, SavedModel)

