from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# Secret key for signing session cookies and other cryptographic operations
SECRET_KEY = '9f2a0b3c4e9d5f8a7c6e1d2b9a0f3c8b5e7d4a9c6f1e2b3d4f8a9b0c7d6e5a9f'

# Session settings
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Session will expire after 30 minutes

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'None'

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
MYSQL_DB = os.getenv('MYSQL_DB', 'mysql_db')
