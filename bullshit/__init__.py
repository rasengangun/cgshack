from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'ONLYFANS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///konf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'posts.html'


from bullshit import models, router

with app.app_context():
    db.create_all()