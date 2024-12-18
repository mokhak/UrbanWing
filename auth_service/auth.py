from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "helloworld"
jwt = JWTManager(app)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["auth_database"]
collection = db["users"]
stats_collection = db["endpoint_stats"]

@app.before_request
def start_timer():
    request.start_time = time.time()  # Record the start time

@app.after_request
def log_response(response):
    execution_time = round(time.time() - request.start_time, 3)  # Time in seconds
    
    # Log the request details, including execution time
    stats_collection.insert_one({
        "service": "auth_service",  # Service name
        "endpoint": request.endpoint or "unknown",
        "method": request.method,
        "status_code": response.status_code,
        "timestamp": datetime.utcnow(),
        "request_ip": request.remote_addr,
        "execution_time": execution_time,  # Log execution time
        "user_agent": request.headers.get("User-Agent")
    })
    return response

@app.route("/authenticate", methods=["GET"])
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    user = collection.find_one({
        "username": username
    })
    
    if user:
        if bcrypt.checkpw(password.encode(), user.get("password").encode()):
            identity={
                "firstname": user.get("firstname"),
                "lastname": user.get("lastname"),
                "email": user.get("email"),
                "role": user.get("role")
            }
            access_token = create_access_token(identity=json.dumps(identity))
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"success": False, "message": "Invalid Credentials!"}), 401
    else:
        return jsonify({"success": False, "message": "Invalid Credentials!"}), 401

@app.route("/createuser", methods=["POST"])
def createuser():
    data = request.json
    first_name = data.get("firstname")
    last_name = data.get("lastname")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    
    insert_data = {
        "firstname": first_name,
        "lastname": last_name,
        "email": email,
        "username": username,
        "password": password,
        "role": "Regular"
    }
    
    existing_user = collection.find_one({
        "$or": [
            {"email": insert_data["email"]},
            {"username": insert_data["username"]}
        ]
    })
    
    if existing_user:
        if existing_user.get("email") == insert_data["email"]:
            return jsonify({"success": False, "message": "Email Fault"}), 401
        if existing_user.get("username") == insert_data["username"]:
            return jsonify({"success": False, "message": "Username Fault"}), 402
    else:
        collection.insert_one(insert_data)
        user_data = collection.find_one({"username": insert_data["username"]})
        return jsonify({"success": True, 
                        "message": "User Registered",
                        "firstname": user_data.get("firstname"),
                        "role": user_data.get("role")
                        }), 200
    
@app.route("/getuserinfo", methods=["GET"])
@jwt_required()
def getuserinfo():
    identity = json.loads(get_jwt_identity())
    
    return jsonify({
        "firstname": identity.get("firstname"),
        "lastname": identity.get("lastname"),
        "email": identity.get("email"),
        "role": identity.get("role")
    }), 200
    
@app.route("/getallusers", methods=["GET"])
@jwt_required()
def getallusers():
    identity = json.loads(get_jwt_identity())
    data = request.json
    
    if identity.get("role") == data.get("role"):
        results = list(collection.find({}, {"_id": 0}))
        return jsonify(results), 200
    else:
        return jsonify({"Unauthorized"}), 403       
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)