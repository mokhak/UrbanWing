from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = {
    "kirat": "1234"
}

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username in USERS and USERS[username] == password:
        return jsonify({"success": True, "message": "Auth Successful!"}), 200
    return jsonify({"success": False, "message": "Invalid Credentials!"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5005)