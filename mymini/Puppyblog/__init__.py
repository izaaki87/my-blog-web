from flask import Flask
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


app.config['SECRET_KEY'] = 'scretke'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, "data.sqlite")
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/profile_pics')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from Puppyblog.users.views import users
from Puppyblog.core.views import core
from Puppyblog.blog_posts.views import blog



app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(blog)
