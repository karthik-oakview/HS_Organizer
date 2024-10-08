from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "dbatabase.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
    app.config['SECRET_KEY'] = 'd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
#    app.config['MAIL_SERVER'] = 'smpt.gmail.com'
#    app.config['MAIL_PORT'] = 465                                                                                                                                                             
#    app.config['MAIL_USERNAME'] = 'karthik.oakview@gmail.com'
#    app.config['MAIL_PASSWORD'] = '*****'
#    app.config['MAIL_USE_TLS'] = False
#    app.config['MAIL_USE_SSL'] = True
    db.init_app(app)

    print('success 1')    

    from .views import views
    from .auth import auth

    print('success 2')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)
                                       
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
   
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))   

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
      with app.app_context():
          db.create_all()
  