from config import db,vuln_by_design
import jwt
import datetime
import os

alive = int(os.getenv('tokentimetolive', 600))


def token_validator(auth_header):
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except:
            auth_token = ""
    else:
        auth_token = ""
    if auth_token:
        return decode_auth_token(auth_token)
    else:
        return "Invalid token"

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=alive),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            vuln_by_design.app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    print("auth_token",auth_token)
    try:
        payload = jwt.decode(auth_token, vuln_by_design.app.config.get('SECRET_KEY'),"HS256")
        return {'uid': payload['sub']}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
  
    

if __name__ == '__main__':
    from models.user_model import User
    from models.webaccess_model import Webaccess
    
    #initialize DB
    db.drop_all()
    db.create_all()
    User.init_db_users()

    vuln_by_design.run(host='0.0.0.0', port=5000, debug=True)
