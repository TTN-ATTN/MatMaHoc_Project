from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

user_api = Blueprint('user_api', __name__)

def DBConnect():
    client = MongoClient("mongodb://localhost:27017/")
    try:
        client.server_info()
    except ServerSelectionTimeoutError:
        client = MongoClient("mongodb://localhost:27017/")
    
    # client.drop_database("user")  # Drop the database if it exists for fresh start
    db = client["user"]
    collection = db['user_data']
    
    collection.create_index([('username', 1)], unique=True)

    admin_user = collection.find_one({'username': 'admin'})
    if admin_user is None:
        admin_user = {
            'user_id': 1,
            'username': 'admin',
            'hash_password': 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec',
            'attribute': '{"ATTR": ["administrator"]}'
        }
        collection.insert_one(admin_user)

    return collection

collection = DBConnect()

@user_api.route('/api/get_user_info', methods=['POST'])
def queryUser():
    if request.method == 'POST':
        username = request.form.get('username')
        
        user_data = collection.find_one({'username': username})

        if user_data:
            server_response = {
                'user_id': user_data['user_id'],
                'username': user_data['username'],
                'hash_password': user_data['hash_password'],
                'attribute': user_data['attribute']
            }

            return jsonify(server_response), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    return "Method Not Allowed", 405

@user_api.route('/api/add_user', methods=['POST'])
def addUser():
    if request.method == 'POST':
        username = request.form.get('username')
        hash_password = request.form.get('password')
        attribute = request.form.get('attribute')

        user_exists = collection.find_one({'username': username})

        if user_exists:
            return jsonify({'error': 'User already exists'}), 400
        else:
            user_data = {
                'user_id': collection.count_documents({}) + 1,
                'username': username,
                'hash_password': hash_password,
                'attribute': attribute
            }

            collection.insert_one(user_data)

            return jsonify({'status': 'success'}), 201
    
    return "Method Not Allowed", 405

@user_api.route('/api/change_password', methods=['POST'])
def changePassword():
    if request.method == 'POST':
        username = request.form.get('username')
        hash_password = request.form.get('new_passwd')

        user_exists = collection.find_one({'username': username})

        if user_exists:
            collection.update_one({'username': username}, {'$set': {'hash_password': hash_password}})
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    
    return "Method Not Allowed", 405