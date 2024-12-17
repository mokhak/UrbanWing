from flask import Flask, request, jsonify
from pymongo import MongoClient
from gridfs import GridFS
import datetime
import uuid
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import json
import requests

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
grid_fs = GridFS(db)

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
            insert_data = {
                "imageid": str(uuid.uuid4()),
                "imageurl": image_url,
                "useremail": data.get("useremail"),
                "timestamp": datetime.datetime.now(),
                "classification_status": False,
                "classification": None 
            }
            collection.insert_one(insert_data)
            return jsonify({"success": "True"}), 200
        else:
            return jsonify("Failed to fetch Image. Status code:", response.status_code)
    else:
        return jsonify({"Unauthorized"}), 403
    
if __name__ == "__main__":
    app.run(debug=True, port=5004)


        
    
