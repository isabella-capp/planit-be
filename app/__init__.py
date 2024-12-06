from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main.bp)

    from .routes import auth
    app.register_blueprint(auth.bp)

    from .routes import dashboard
    app.register_blueprint(dashboard.bp)

    from .routes import db_route
    app.register_blueprint(db_route.bp, url_prefix='/db')
    
    return app