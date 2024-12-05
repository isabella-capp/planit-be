from flask import Flask

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

    from .routes import db_route
    app.register_blueprint(db_route.bp, url_prefix='/db')
    
    return app