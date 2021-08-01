from config import db, vuln_by_design
from api_views.schemas import *
from flask import jsonify, Response, request, json
from app import *
from models.webaccess_model import Webaccess

def get_webaccess_by_user(user_id):
    #API1:2019 — Broken object level authorization
    return_value = jsonify({'webacess': Webaccess.get_url_by_user(user_id)})
    return return_value

