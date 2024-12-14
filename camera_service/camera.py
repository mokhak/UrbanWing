from flask import Flask, request, jsonify
from pymongo import MongoClient
from gridfs import GridFS
import datetime
import uuid

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["image_database"]
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


        
    
