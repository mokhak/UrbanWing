from flask import Flask, request, jsonify
from pymongo import MongoClient, DESCENDING
import uuid
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
import json
import requests
import time
from datetime import datetime
ML_SERVICE_URL = "http://159.89.235.193:5003"

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
        "service": "camera_service",  # Service name
        "endpoint": request.endpoint or "unknown",
        "method": request.method,
        "status_code": response.status_code,
        "timestamp": datetime.utcnow(),
        "request_ip": request.remote_addr,
        "execution_time": execution_time,  # Log execution time
        "user_agent": request.headers.get("User-Agent")
    })
    return response

@app.route("/upload-image", methods=["POST"])
@jwt_required()
def upload_image():
    identity = json.loads(get_jwt_identity())
    data = request.json
    
    if identity.get("role") == data.get("role"):
        response = requests.get(f"{unsplash_url}&client_id={unsplash_access_key}")
        if response.status_code == 200:
            response = response.json()
            image_url = response["urls"]["regular"]
            image_id = str(uuid.uuid4())
            insert_data = {
                "imageid": image_id,
                "imageurl": image_url,
                "useremail": data.get("useremail"),
                "timestamp": datetime.now(),
                "classification_status": False,
                "classification": None 
            }
            collection.insert_one(insert_data)
            header = request.headers.get("Authorization")
            headers = {"Authorization": header}
            response = requests.get(
                ML_SERVICE_URL + '/classify-image',
                headers=headers,
                json={"role": data.get("role"),
                      "imageid": image_id}
            )
            if response.status_code == 200:
                return jsonify({"success": "True"}), 200
            else:
                return jsonify({"error": "Cannot Classify Image"}), response.status_code
        else:
            return jsonify({"error": "Failed to fetch image"}), response.status_code
    else:
        return jsonify({"Unauthorized"}), 403
    
@app.route("/get-latest-visitor", methods=["GET"])
@jwt_required()
def get_latest_visitor():
    identity = json.loads(get_jwt_identity())
    data = request.json
    
    if identity.get("email") == data.get("email"):
        query = {"useremail": data.get("email")}
        latest_entry = collection.find_one(query, sort=[("timestamp", DESCENDING)])
        if not latest_entry:
            return jsonify({"message": "No Entries"}), 404
        
        result = {
            "imageurl": latest_entry.get("imageurl"),
            "classification_status": latest_entry.get("classification_status"),
            "classification": latest_entry.get("classification")
        }
        return jsonify(result), 200
    else:
        return jsonify({"error":"Not authorized!"}), 500
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    app.run(host="0.0.0.0", port=port)