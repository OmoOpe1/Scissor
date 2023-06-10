from datetime import datetime
from src import db, login_manager
from flask_login import UserMixin
from werkzeug.exceptions import NotFound


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Url(db.Model):
    __tablename__='url'
    id = db.Column(db.Integer(), primary_key=True)
    link = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Url {self.link}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def get_by_link(cls, link):
        url = cls.query.filter_by(link=link).first()
        return url

class Short(db.Model):
    __tablename__='short'
    id = db.Column(db.Integer(), primary_key=True)
    alias = db.Column(db.String(128), nullable=False)
    hits = db.Column(db.Integer(), default=0)
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    url = db.relationship("Url")

    @classmethod
    def get_by_alias(cls, alias):
        short_url = cls.query.filter_by(alias=alias).first()
        return short_url
    
    def __repr__(self) -> str:
        return f"<Short {self.alias}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def increment_hits(self):
        self.hits = self.hits + 1
        db.session.commit()
 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    short_urls = db.relationship('Short', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


