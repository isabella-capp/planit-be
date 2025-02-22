from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    
    from . import db
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main.bp)

    from .routes import auth
    app.register_blueprint(auth.bp)

    from .routes import event
    app.register_blueprint(event.bp)
    
    from .routes import availability
    app.register_blueprint(availability.bp)
    
    return app