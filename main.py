from flask import Flask, request, jsonify, send_file, url_for
import sqlite3
import requests
import os

app = Flask(__name__)




@app.route("/")
def index():
    data = {
        "response": "Welcome to EXE API!",
        "msg": "Invalid parameters"
    }

    return jsonify(data), 400


@app.route("/api/v1/messages/<message_id>", methods=["POST"])
def messages(message_id):
    if request.method == "POST":
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        message_data = {
            "message_id": message_id,
        }
        message_content = request.args.get("content")
        if message_content:
            message_data["message_content"] = message_content
        
        author = request.args.get("author")
        if author:
            message_data["author"] = author
        
        user_id = request.args.get("user_id")
        if user_id:
            message_data["user_id"] = user_id
        
        timestamp = request.args.get("timestamp")
        if timestamp:
            message_data["timestamp"] = timestamp
        
        query = "INSERT INTO messages (author_id, message_id, message, timestamp) VALUES (?, ?, ?, ?)"
        values = (author, message_id, message_content, timestamp,)
        cur.execute(query, values)
        conn.commit()
        
        
        
        return jsonify(message_data), 201

@app.route("/status", methods=["GET"])
def get_status():
    url = "https://basic-nextjs-webjd-m7ri.vercel.app/"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = {
                "status": 200,
                "description": "App Running"
            }

            return jsonify(data), 200
        if response.status_code == 400:
            data = {
                "status": 400,
                "description": "Website not running, offline"
            }
            return jsonify(data), 200
        else:
            data = {
                "status": 500,
                "description": "The website doesn't exists, ERROR"
            }
            return jsonify(data), 200
    except:
        return "A error occurred", 500
    

@app.route("/api/v1/messages/<message_id>")
def get_message(message_id):
    try:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        query = "SELECT * FROM messages WHERE message_id = ?"
        values = (message_id,)
        cur.execute(query, values)
        fetch = cur.fetchall()

        message_content = []
        for message in fetch:
            data = {
                "author_id": message[0],
                "message_id": message[1],
                "message": message[2],
                "timestamp": message[3]
            }
            message_content.append(data)
        conn.close()
        return jsonify(message_content), 200
    except sqlite3.Error as e:
        conn.close()
        status = {
            "status": "ERROR",
            "desc": f"Error {str(e)}"
        }

        return jsonify(status), 500

@app.route("/downloads", methods=["GET"])
def download():
    path = "./files"
    files = os.listdir(path)
    return "\n".join(files)

@app.route("/downloads/<filename>", methods=["GET"])
def download_file(filename):
    path = "C:/Users/jcoso/OneDrive/Documentos/Full API comunicate with DBS/files"
    file = os.path.join(path, filename)
    return send_file(file, as_attachment=True)

@app.route("/view-file/<filename>", methods=["GET"])
def view_file(filename):
    path = "C:/Users/jcoso/OneDrive/Documentos/Full API comunicate with DBS/files"
    file = os.path.join(path, filename)
    return send_file(file)

@app.route("/api/v1/user-info/<user_id>", methods=["GET"])
def get_user_info(user_id):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    query = "SELECT * FROM users WHERE user_id = ?"
    values = (user_id,)

    cur.execute(query, values)

    fetch = cur.fetchall()
    user_info = []
    for user in fetch:
        data = {
            "Discord Name": user[0],
            "Join Date": user[1],
            "Acc Created at": user[2]
        }
        user_info.append(data)

@app.route("/api/v1/add-user/<user_id>", methods=["GET", "POST"])
def add_user(user_id):
    if request.method == "GET":
        data = {
            "status": "ERROR",
            "msg": "Cannot GET a POST request"
        }
        return jsonify(data), 405
    if request.method == "POST":
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        data = {
            "user_id": user_id,
        }

        discordname = request.args.get("discord_name")
        if discordname:
            data["discord_name"] = discordname
        
        joined = request.args.get("joined_at")
        if joined:
            data["joined"] = joined
        
        created_at = request.args.get("created_at")
        if created_at:
            data["created_at"] = created_at
        
        query = "INSERT INTO userinfo (user_id, discord_name, joined_at, acc_created_at) VALUES (?,?,?,?)"
        values = (user_id, discordname, joined, created_at,)
        cur.execute(query, values)
        return jsonify(data), 201

@app.route("/api/v2/smx", methods=["GET", "POST"])
def download_smx():
    if request.method == "GET":
        path = os.path.join(".", "files")
        files = os.listdir(path)
        links = []
        for file in files:
            if os.path.isdir(os.path.join(path, file)):
                links.append(f"<a href='/api/v2/smx/{file}'>{file}</a>")
            else:
                links.append(f"<a href='/api/v2/smx/{file}'>{file}</a>")
        return "</br>".join(links), 200
    if request.method == "POST":
        data = {
            "msg": "Still working on this"
        }
        return data, 401
    

@app.route("/api/v2/smx/<path:folder>", methods=["GET", "POST"])
def browse_subdir(folder):
    path = os.path.join(".", "files", folder)
    links = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, path)
            if os.path.isdir(filepath):
                links.append(f'<a href="{url_for("browse_subdir", folder=os.path.join(folder, relative_path))}">{relative_path}/</a>')
            else:
                links.append(f'<a href="{url_for("download_file_smx", filename=os.path.join(folder, relative_path))}">{relative_path}</a>')
    return "<br>".join(links)

@app.route("/api/v2/smx/download_file/<path:filename>")
def download_file_smx(filename):
    # directory = os.path.join(".", "files")
    # return send_from_directory(directory, filename, as_attachment=True)
    data = {
        "status": "DOWN",
        "msg": "We have issues with this service please wait to get fixed"
    }

    return jsonify(data), 401

@app.route("/api/v9/bots/<bot_id>", methods=["GET"])
def bot_status(bot_id):
    data = {
        "bot_id": bot_id
    }

    status = request.args.get("status")
    if status:
        data["status"] = status
    
    return jsonify(data), 200
