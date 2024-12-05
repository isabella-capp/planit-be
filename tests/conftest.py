import os
import pytest
from app.factory import create_app
from app.db import get_db, init_db

from dotenv import load_dotenv

load_dotenv()

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

def init_test_db(app):
    init_db()
    try:
        db_test = get_db()
        cur = db_test.cursor()

        for command in _data_sql.split(';'):
            if command.strip():
                cur.execute(command)

        db_test.commit()
    except Exception as e:
        db_test.rollback()
        app.logger.error(f"Failed to initialize the database: {e}")
        raise
    finally:
        cur.close()

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'MYSQL_DB': 'test_db',
        'MYSQL_HOST': '127.0.0.1',
        'MYSQL_PORT': int(os.getenv('MYSQL_PORT', 3306)),
        'MYSQL_USER': os.getenv('MYSQL_USER', 'root'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD', 'root')
    })

    with app.app_context():
        init_test_db(app)

    yield app 


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
