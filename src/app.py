"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")  # Create the jackson family object


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_members():
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                    "family": members}
    return jsonify(response_body), 200

@app.route('/members<int:member_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_members(member_id):
    response_body = {'id': '',
                    'name': '',
                    'age': '',
                    'lucky_numbers': []}
    if request.method == 'GET':
        row = jackson_family.get_member(member_id)
        print(row)
        response_body['message'] = 'Usuario seleccionado'
        response_body['results'] = member_id
        return response_body, 200
    
    if request.method == 'PUT':
        jackson_family[member_id] = request.json
        response_body['message'] = f'Member {member_id} edited'
        response_body['results'] = jackson_family[member_id]
        return response_body, 200

    if request.method == 'DELETE':
        jackson_family.delete_member(member_id)
        response_body = {"message": "Member deleted"}
        return jsonify(response_body), 200


# @app.route('/members', methods=['POST'])
# def handle_members():
#     response_body = {'id': '',
#                     'name': '',
#                     'age': '',
#                     'lucky_numbers': []}
#     if request.method == 'POST':
#         data = request.json
#         members.append(data)
#         response_body['message'] = 'Usuario agregado exitosamente'
#         response_body['results'] = members
#         return jsonify(response_body), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
