from flask import Flask, request, jsonify
from pymongo import MongoClient
from gridfs import GridFS
import datetime
import uuid
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "helloworld"
jwt = JWTManager(app)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["auth_database"]
collection = db["images"]
grid_fs = GridFS(db)

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files["image"]
    
    unique_name = f"{uuid.uuid1()}_{image_file.filename}"
    
    try:
        file_id = grid_fs.put(
            image_file,
            filename=unique_name,
            timestamp=datetime.datetime.now()
        )
        return jsonify({
            "message": "Image uploaded successfully",
            "file_id": str(file_id),
            "filename": unique_name,
            "timestamp": datetime.datetime.now().isoformat()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5004)


        
    
