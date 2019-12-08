from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.run(debug=True, host='0.0.0.0')
app.config.from_object(Config)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.session_protection = 'strong'
login.login_view = 'login'

from app import routes, models

if not models.User.query.filter_by(username='admin').first():
    user = models.User(username=os.environ.get('ADMIN_USER'))
    user.set_two_factor(os.environ.get('ADMIN_MFA'))
    user.set_password(os.environ.get('ADMIN_PASSWORD'))
    user.set_admin(True)
    db.session.add(user)
    db.session.commit()