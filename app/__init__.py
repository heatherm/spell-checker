from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_seeder import FlaskSeeder

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# seeder = FlaskSeeder()
# seeder.init_app(app, db)

login = LoginManager(app)
login.session_protection = "strong"
login.login_view = 'login'

from app import routes, models
