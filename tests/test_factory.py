from flask import Flask
from app.factory import create_app

def test_config():
    """ Test the create_app function with different configurations. """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_app_exists(app):
    """Test that the app factory creates an app instance."""
    assert app is not None
    assert isinstance(app, Flask)

def test_main_blueprint_registered(app):
    """Test that the main blueprint is registered."""
    assert "main" in app.blueprints

def test_db_blueprint_registered(app):
    """Test that the db blueprint is registered."""
    assert "db" in app.blueprints
