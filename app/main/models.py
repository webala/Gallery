from email.policy import default
from app import db, login_manager
from flask_login import UserMixin
from werkzeug import security 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    profile_picture = db.Column(db.String(20), nullable=True, default='profile-avatar.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return self.username

    def generate_password_hash(self, password):
        return security.generate_password_hash(password)

    def check_password_hash(self, password):
        return security.check_password_hash(self.password, password)


class ArtWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_work = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(20), nullable=True)
    on_display = db.Column(db.Boolean, default=True, nullable=True)