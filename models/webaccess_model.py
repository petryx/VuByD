
from sqlalchemy.orm import relationship
from config import db, vuln_by_design
from app import  alive
from random import randrange
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime


class Webaccess(db.Model):
    __tablename__ = 'webaccess'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(500), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime,unique=False, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="webaccess")

    def __repr__(self):
        return f"<User(url={self.url}, user={self.user})>"

    def json(self):
        return {'url': self.url, 'user': self.user.username, 'timestamp': self.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')}    
    
    @staticmethod
    def get_url_by_user(user_id):
        return [Webaccess.json(user) for user in Webaccess.query.filter(Webaccess.user_id==user_id)]

    @staticmethod
    def get_all_urls():
        return [Webaccess.json(user) for user in Webaccess.query.all()]

    @staticmethod
    def register_user(url, timestamp, user):
        new_webaccess = Webaccess(url=url, timestamp=timestamp, user_id=user.id)
        db.session.add(new_webaccess)
        db.session.commit()
