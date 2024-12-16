from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

mongo_uri = "mongodb+srv://mokhak:6u5SGOTuvd0IYKIw@uwcluster.mj1rh.mongodb.net/?retryWrites=true&w=majority&appName=UWCluster"
client = MongoClient(mongo_uri)
db = client["auth_database"]
collection = db["users"]

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    user = collection.find_one({
        "username": username
    })
    
    if user:
        if bcrypt.checkpw(password.encode(), user.get("password").encode()):
            return jsonify({"success": True, 
                            "firstname": user.get("firstname"),
                            "role": user.get("role"),
                            "message": "Auth Successful!"}), 200
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
    
    

if __name__ == "__main__":
    app.run(debug=True, port=5005)