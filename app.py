from flask import Flask, request, jsonify
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load the models
image_model = tf.keras.models.load_model('C:/Users/sri/deepfake-detectionnew/backend/models/cnn_image_model.keras')
tweet_model = tf.keras.models.load_model('C:/Users/sri/deepfake-detectionnew/backend/models/distilbert_tweet_model.keras')
tokenizer = tf.keras.models.load_model('C:/Users/sri/deepfake-detectionnew/backend/models/distilbert_tweet_model.keras')

# Initialize Flask app
app = Flask(__name__)

# Image prediction endpoint
@app.route('/predict_image', methods=['POST'])
def predict_image():
    img = request.files['image']
    img = Image.open(img)
    img = img.resize((128, 128))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = image_model.predict(img)
    result = 'Real' if prediction[0][0] > 0.5 else 'Fake'

    return jsonify({'prediction': result})

# Tweet prediction endpoint
@app.route('/predict_tweet', methods=['POST'])
def predict_tweet():
    tweet = request.json['tweet']
    inputs = tokenizer(tweet, return_tensors="tf", padding=True, truncation=True, max_length=128)
    outputs = tweet_model(inputs)
    prediction = np.argmax(outputs.logits, axis=-1)[0]

    result = 'Real' if prediction == 1 else 'Fake'
    return jsonify({'prediction': result})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  