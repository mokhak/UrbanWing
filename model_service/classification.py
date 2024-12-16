import os
import random
from flask import Flask, request, jsonify
from pymongo import MongoClient
from gridfs import GridFS

from transformers import AutoFeatureExtractor, AutoModelForImageClassification

extractor = AutoFeatureExtractor.from_pretrained("chriamue/bird-species-classifier")
model = AutoModelForImageClassification.from_pretrained("chriamue/bird-species-classifier")


app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client['image_database']
grid_fs = GridFS(db)

# Mock bird predictions
BIRD_CLASSES = [
    "Sparrow",
    "Robin",
    "Crow",
    "Eagle",
    "Hawk",
    "Pigeon",
    "No bird detected"
]

@app.route("/classify-image", methods=["POST"])
def classify_image():
    data = request.json
    image_name = data.get("image_name")
    
    try:
        image_data = grid_fs.find_one({"filename": image_name})
        if not image_data:
            return jsonify({"error": "Image not found in the database!"})
            
        bird_type = random.choice(BIRD_CLASSES)
        confidence = round(random.uniform(0.5, 1.0), 2)
        bird_detected = bird_type != "No bird detected"
        
        db.fs.files.update_one(
            {"filename": image_name},
            {
                "$set": {
                    "bird_detected": bird_detected,
                    "bird_type": bird_type,
                    "confidence": confidence
                }
            }
        )
        
        return jsonify({
            "bird_detected": bird_detected,
            "bird_type": bird_type,
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5003)