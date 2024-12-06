from dotenv import load_dotenv
import os

def load_env_file(file_path):
    if os.path.exists(file_path):
        load_dotenv(dotenv_path=file_path)
    else:
        print(f"Warning: {file_path} not found.")

load_env_file('.env')

SECRET_KEY = 'secret'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'None'

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
MYSQL_DB = os.getenv('MYSQL_DB', 'mysql_db')