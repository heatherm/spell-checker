from app import db, login, bcrypt
from flask_login import UserMixin
from flask_bcrypt import check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    two_factor = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def set_two_factor(self, two_factor):
        self.two_factor = bcrypt.generate_password_hash(two_factor)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_two_factor(self, two_factor):
        return check_password_hash(self.two_factor, two_factor)


class Qqquery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(256), index=True, unique=False)
    output = db.Column(db.String(256), index=True, unique=False)
    user_id = db.Column(db.Integer, index=True, unique=False)

    def __repr__(self):
        return '<Qqquery {}>'.format(self.id)
