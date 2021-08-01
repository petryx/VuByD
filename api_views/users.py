import re
import jsonschema
import jwt

from config import db, vuln_by_design
from api_views.schemas import *
from flask import jsonify, Response, request, json
from models.user_model import User
from app import *


def error_message_helper(msg):
    return '{ "status": "fail", "message": "' + msg + '"}'

def get_by_email(email):
    
    if User.get_user(email):
        return Response(str(User.get_user(email)), 200, mimetype="application/json")
    else:
        return Response(error_message_helper("User not found"), 404, mimetype="application/json")

def whoami():
    resp = token_validator(request.headers.get('Authorization'))
    user = User.query.filter_by(username=resp['uid']).first()
    return_value = jsonify({'users': user.json()})
    return return_value

def register_user():
    request_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(username=request_data.get('username')).first()
    if not user:
        try:
            # validate the data are in the correct form
            jsonschema.validate(request_data, register_user_schema)
            
            #API6: 2019 Mass Assignment
            content = request.get_json(silent=True)
            user = User(**content)
            db.session.add(user)
            db.session.commit()

            responseObject = {
                'status': 'success',
                'message': 'Successfully registered. Login to receive an auth token.'
            }

            return Response(json.dumps(responseObject), 200, mimetype="application/json")
        except jsonschema.exceptions.ValidationError as exc:
            return Response(error_message_helper(exc.message), 400, mimetype="application/json")
    else:
        return Response(error_message_helper("User already exists. Please Log in."), 200, mimetype="application/json")

def login_user():
    request_data = request.get_json()

    try:
        # validate the data are in the correct form
        jsonschema.validate(request_data, login_user_schema)
        # fetching user data if the user exists
        user = User.query.filter_by(username=request_data.get('username')).first()
        if user and request_data.get('password') == user.password:
            auth_token = encode_auth_token(user.username)
            
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token
            }
            return Response(json.dumps(responseObject), 200, mimetype="application/json")
        if user and request_data.get('password') != user.password: # Password BruteForce
            return Response(error_message_helper("Password is not correct for the given username."), 200, mimetype="application/json")
        elif not user:  # User enumeration
            return Response(error_message_helper("Username does not exist"), 200, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        return Response(error_message_helper(exc.message), 400, mimetype="application/json")

def update_email():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, update_email_schema)
    except:
        return Response(error_message_helper("Please provide a proper JSON body."), 400, mimetype="application/json")
    resp = token_validator(request.headers.get('Authorization'))
    user = User.query.filter_by(username=resp['uid']).first()
    #Evil Regexes REDOS
    match = re.search(
            r"^([0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*@{1}([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$",
            str(request_data.get('email')))
    if match:
        user.email = request_data.get('email')
        db.session.commit()
        responseObject = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email
                }
            }
        return Response(json.dumps(responseObject), 204, mimetype="application/json")
    else:
        return Response(error_message_helper("Please Provide a valid email address."), 400, mimetype="application/json")
    
def update_password(username):
    request_data = request.get_json()
    if request_data.get('password'):
        #API5:2019 — Broken function level authorization
        user = User.query.filter_by(username=username).first()
        user.password = request_data.get('password')
        db.session.commit()
        responseObject = {
            'status': 'success',
            'Password': 'Updated.'
        }
        return Response(json.dumps(responseObject), 204, mimetype="application/json")
    else:
        return Response(error_message_helper("Malformed Data"), 400, mimetype="application/json")

def delete_user(username):
    resp = token_validator(request.headers.get('Authorization'))
    user = User.query.filter_by(username=resp['uid']).first()
    if user.is_admin:
        if username == 'admin':
            return Response(error_message_helper("Opss Internal Error!"), 500, mimetype="application/json")
        elif resp['uid'] == user.username:
            return Response(error_message_helper("Opss Internal Error!"), 500, mimetype="application/json")
        elif bool(User.delete_user(username)):
            responseObject = {
                'status': 'success',
                'message': 'User deleted.'
            }
            return Response(json.dumps(responseObject), 200, mimetype="application/json")
        else:
            return Response(error_message_helper("User not found!"), 404, mimetype="application/json")
    else:
        return Response(error_message_helper("Only Admins may delete users!"), 401, mimetype="application/json")

