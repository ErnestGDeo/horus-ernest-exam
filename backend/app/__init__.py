from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, bcrypt, cors
from app.routes.users import users_bp
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    Swagger(app)

    # Register blueprint
    from app.routes import users
    app.register_blueprint(users_bp)

    return app
