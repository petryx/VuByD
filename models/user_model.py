
from datetime import datetime, timedelta
from models.webaccess_model import Webaccess
from sqlalchemy.orm import relationship
from config import db, vuln_by_design
from app import  alive
from random import randrange

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    webaccess = relationship("Webaccess", order_by=Webaccess.id, back_populates="user")

    def __repr__(self):
        return f"<User(name={self.username}, email={self.email})>"

    def json(self):
        return{'username': self.username, 'email': self.email}

    def json_debug(self):
        return{'username': self.username, 'password': self.password, 'email': self.email, 'admin': self.admin}

    @staticmethod
    def get_all_users():
        return [User.json(user) for user in User.query.all()]

    @staticmethod
    def get_all_users_debug():
        return [User.json_debug(user) for user in User.query.all()]

    @staticmethod
    def get_user(email):
        # API8:2019 — Injection SQLi Injection 
        user_query = f"SELECT * FROM users WHERE email = '{email}'"
        query = db.session.execute(user_query)
        ret = query.fetchone()
        if ret:
            fin_query = '{"username": "%s", "email": "%s","is_admin": "%s"}' % (ret[1], ret[3],ret[4])
        else:
            fin_query = None
        return fin_query

    @staticmethod
    def register_user(username, password, email, is_admin=False):
        new_user = User(username=username, password=password, email=email, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def delete_user(username):
        done = User.query.filter_by(username=username).delete()
        db.session.commit()
        return done

    @staticmethod
    def init_db_users():
        user1 = User.register_user("john", "jhon_Super_Pass2021", "john@vubyd.com", False)
        user2 = User.register_user("maria", "maria2021", "maria@vubyd.com", False)
        User.register_user("admin", "admin_ssaP_1202", "admin@vubyd.com", True)
        Webaccess.register_user("https://google.com", datetime.now() - timedelta(days=5), user1)
        Webaccess.register_user("https://facebook.com", datetime.now() - timedelta(days=1), user1)
        Webaccess.register_user("https://xxxx.com", datetime.now() - timedelta(days=10), user1)
        Webaccess.register_user("https://twitter.com", datetime.now() - timedelta(days=15), user2)
        Webaccess.register_user("https://youtube.com", datetime.now() - timedelta(days=11), user2)
        Webaccess.register_user("https://xxxx.com", datetime.now() - timedelta(days=2), user2)
        


