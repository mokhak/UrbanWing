from flask import Flask, request, jsonify
from pymongo import MongoClient, DESCENDING
from gridfs import GridFS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import json
import requests
import random
import time
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "helloworld"
jwt = JWTManager(app)

mongo_uri = os.getenv("MONGO_URI")
unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY")
unsplash_url = os.getenv("UNSPLASH_API_URL")

client = MongoClient(mongo_uri)
db = client["auth_database"]
collection = db["images"]
stats_collection = db["endpoint_stats"]

@app.before_request
def start_timer():
    request.start_time = time.time()  # Record the start time

@app.after_request
def log_response(response):
    execution_time = round(time.time() - request.start_time, 3)  # Time in seconds
    
    # Log the request details, including execution time
    stats_collection.insert_one({
        "service": "ml_model_service",  # Service name
        "endpoint": request.endpoint or "unknown",
        "method": request.method,
        "status_code": response.status_code,
        "timestamp": datetime.utcnow(),
        "request_ip": request.remote_addr,
        "execution_time": execution_time,  # Log execution time
        "user_agent": request.headers.get("User-Agent")
    })
    return response

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

@app.route("/classify-image", methods=["GET"])
@jwt_required()
def classify_image():
    identity = json.loads(get_jwt_identity())
    data = request.json
    image_name = {"imageid": data.get("imageid")}
    
    if identity.get("role") == data.get("role"):
        bird_type = random.choice(BIRD_CLASSES)
        insert_data = {
            "classification_status": True,
            "classification": bird_type
        }
        collection.update_one(image_name, {"$set":insert_data})
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5003)