from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

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
    user = models.User(username='admin')
    user.set_two_factor('12345678901')
    user.set_password('Administrator@1')
    user.set_admin(True)
    db.session.add(user)
    db.session.commit()