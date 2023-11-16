import sqlite3
import json
from flask import Flask, request, jsonify
from flask_cors import CORS 

DB_PATH = './DB/data.db'

# api 
app = Flask("__name__")
CORS(app, resources=r'/api/*')

#utils
def gen_response(data):
    response = {
            "data": data
        }
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

''' METHODS AND APIS FOR USERS  '''
#users CRUD -> In GET don't gather image, do it with another method
def get_all_users(): 
    query = f"""SELECT user_id, username, descr, status, avatar
    FROM users where status != 'Deleted' """
    
    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    user_details = list(cursor.execute(query))
    response = {
            "data": []
        }
    for user in user_details:
        current_user = {
            "user_id": user[0],
            "username": user[1],
            "descr": user[2],
            "status": user[3],
            "avatar": user[4],
            "hasImage": user[4] != None
        }
        response["data"].append(current_user)
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*") 
    connection.close()
    return response

def get_user(user_id): 
    query = f"""SELECT user_id, username, email, phone, descr, status, timestamp
    FROM users where user_id='{user_id}'"""
    
    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    user_details = list(cursor.execute(query))[0]
    data = {}
    data["user_id"] = user_details[0]
    data["username"] = user_details[1]
    data["email"] = user_details[2]
    data["phone"] = user_details[3]
    data["descr"] = user_details[4]
    data["status"] = user_details[5]
    json_data = json.dumps(data)
    connection.close()
    return json_data

def get_user_avatar(user_id):
    query = f"""SELECT avatar
    FROM users where user_id='{user_id}'"""
    
    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    user_details = list(cursor.execute(query))[0]
    data = {}
    data["avatar"] = user_details[0]
    data["hasImage"] = user_details[0] != None
    json_data = json.dumps(data)
    connection.close()
    return json_data

def login(email, password):
    query = f"""SELECT user_id, username, email, phone, descr, status, timestamp
    FROM users where email='{email}' and password='{password}'"""
    
    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    user_details = list(cursor.execute(query))[0]
    data = {}
    data["user_id"] = user_details[0]
    data["username"] = user_details[1]
    data["email"] = user_details[2]
    data["status"] = user_details[5]
    json_data = json.dumps(data)
    connection.close()
    return json_data

def create_user(username, email, password):
    query = f"""INSERT INTO users(username, email, password, status)
    VALUES('{username}', '{email}', '{password}', 'Active')"""

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    data = {}
    data["user_id"] = cursor.lastrowid
    data["username"] = username
    data["email"] = email
    json_data = json.dumps(data)
    connection.close()
    return json_data

def update_user(user_id, username, email, phone, descr):
    query = f"""UPDATE users
    SET username = '{username}', email = '{email}', phone = '{phone}', descr = '{descr}'  where user_id='{user_id}' or email = '{email}'"""

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def update_picture(user_id, avatar):
    query = f"""UPDATE users
    SET avatar = '{avatar}'  where user_id='{user_id}'"""

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def ban_user(user_id):
    query = f"""UPDATE users
    SET status = 'Banned' where user_id='{user_id}'"""

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def unban_user(user_id):
    query = f"""UPDATE users
    SET status = 'Active' where user_id='{user_id}'"""

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def delete_user(user_id):
    query = f"""UPDATE users
    SET status = 'Deleted' where user_id='{user_id}'"""

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

#  CRUD operations posts
def create_post(user_id, title, type, text):
    query = f"""INSERT INTO posts(user_id, title, type, text, status)
    VALUES('{user_id}', '{title}', '{type}', '{text}', 'Active')"""
    
    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def create_image_post(user_id, title, type, text, image):
    query = f"""INSERT INTO posts(user_id, title, type, text, status, image)
    VALUES('{user_id}', '{title}', '{type}', '{text}','Active', '{image}')"""

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def get_all_posts(offset):
    query = f"""
        SELECT users.username, post_id, posts.user_id, title, type, text, posts.status, image, users.avatar
        FROM posts JOIN users on users.user_id = posts.user_id
        where posts.status != 'Deleted' and users.status != 'Deleted' LIMIT 5 offset '{offset}'"""
    
    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    post_details = list(cursor.execute(query))
    response = {
            "data": []
        }
    for post in post_details:
        if(post[4] == "text"):
            current_user = {
                "user_id": post[3],
                "username": post[0],
                "text": post[5],
                "title": post[3],
                "type": post[4],
                "avatar": post[8],
                "hasAvatar": post[8] != None
            }
            response["data"].append(current_user)
        if(post[4] == "image"):
            current_user = {
                "user_id": post[3],
                "username": post[0],
                "image": post[7],
                "title": post[3],
                "type": post[4],
                "hasImage": post[7] != None,
                "avatar": post[8],
                "hasAvatar": post[8] != None
            }
            response["data"].append(current_user)
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*") 
    connection.close()
    return response

def get_user_posts(user_id):
    query = f"""
        SELECT users.username, post_id, posts.user_id, title, type, text, posts.status, image
        FROM posts JOIN users on users.user_id = posts.user_id
        where posts.status != 'Deleted' and users.status != 'Deleted' and posts.user_id = '{user_id}' """
    
    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    post_details = list(cursor.execute(query))
    response = {
            "data": []
        }
    
    for post in post_details:
        if(post[4] == "text"):
            current_user = {
                "user_id": post[3],
                "username": post[0],
                "text": post[5],
                "title": post[3],
                "type": post[4]
            }
            response["data"].append(current_user)
        if(post[4] == "image"):
            current_user = {
                "user_id": post[3],
                "username": post[0],
                "image": post[7],
                "title": post[3],
                "type": post[4],
                "hasImage": post[7] != None
            }
            response["data"].append(current_user)
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*") 
    connection.close()
    return response

def delete_post(post_id):
    query = f"""UPDATE posts
    SET status = 'Deleted' where post_id = '{post_id}' """

    connection = sqlite3.connect(DB_PATH, timeout= 3.0)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

# Routing 
@app.route("/api/users", methods=["GET", "POST", "PATCH", "DELETE"])
def users():
    try:
        if request.method == "GET":
            users = get_all_users()
            return users, 200
            #user_details = get_user_by_mail(body["email"]);
            #return gen_response(user_details), 200
            #return gen_response("Not implemented"), 500

        if request.method == "POST":
            body = request.json 
            if(body["operation"] == 'signup'):
                if(len(body["username"]) < 4 or len(body["email"]) < 6):
                    return gen_response("Bad credentials"), 400
                if(len(body["password"]) < 3):
                    return gen_response("Password is too short, try a longer one"), 400
                if(body["password"] == body["rep_password"]):
                    data = create_user(body["username"], body["email"], body["password"])
                    return gen_response(data), 200
            if(body["operation"] == 'login'):
                user_details = login(body["email"], body["password"]);
                return gen_response(user_details), 200
            if(body["operation"] == 'id'):
                user_details = get_user(body["user_id"]);
                return gen_response(user_details), 200
            if(body["operation"] == "ppicture"):
                user_details = get_user_avatar(body["user_id"]);
                return gen_response(user_details), 200
            return gen_response("Bad request, retry, I'm lazy to write a better error"), 400

        if request.method == "PATCH":
            body = request.json 
            if(body["operation"] == "id"):
                update_user(body["user_id"], body["username"], body["email"], body["phone"], body["descr"])
                return gen_response("ok"), 200
            if(body["operation"] == "picture"):
                update_picture(body["user_id"], body["avatar"])
                return gen_response("ok"), 200
            return gen_response("Bad password, retype"), 400
        
        if request.method == "DELETE":
            body = request.json 
            if(body["operation"] == 'delete'):
                delete_user(body["user_id"])
            if(body["operation"] == 'ban'):
                ban_user(body["user_id"])
            if(body["operation"] == 'unban'):
                unban_user(body["user_id"])
            return gen_response("ok"), 200
        
    except Exception as e:
        response = {
                "data": None,
                "error": f"Failed to get users. Reason: {e}"
            } 
        response = jsonify(response)
        response.headers.add("Access-Control-Allow-Origin", "*") 
        return response, 500

''' METHODS AND APIS FOR POSTS  '''
@app.route("/api/posts", methods=["GET", "POST", "PATCH", "DELETE"])
def posts():
    try:
        if request.method == 'GET':
           return gen_response("Bad method"), 400

        if request.method == 'POST':
            body = request.json
            if(body["operation"] == "create"):
                if( body["type"] == "text"):
                    create_post(body["user_id"], body["title"], body["type"], body["text"])
                    return gen_response("Ok"), 200
                if( body["type"] == "image"):
                    create_image_post(body["user_id"], body["title"], body["type"], body["text"], body["image"])
                    return gen_response("Ok"), 200
            if(body["operation"] == "get_all"):
                body = request.json
                posts = get_all_posts(body['offset'])
                return posts, 200
            if(body["operation"] == "get_personal"):
                body = request.json
                posts = get_user_posts(body['user_id'])
                return posts, 200
            return gen_response("Bad operation"), 400
        
        if request.method == 'PATCH':
            return gen_response("Not implemented yet"), 500
        if request.method == "DELETE":
            body = request.json
            delete_post(body["post_id"])
            return gen_response("Ok"), 200
        return gen_response("Bad request"), 500

    except Exception as e:
        response = {
                "data": None,
                "error": f"Failed to get users. Reason: {e}"
            } 
        response = jsonify(response)
        response.headers.add("Access-Control-Allow-Origin", "*") 
        return response, 500

if __name__ == "__main__":
     app.debug = True
     app.run(host="0.0.0.0", port=8080, threaded = True)
    
