import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_MY_USER_NAME = os.getenv('GITHUB_MY_USER_NAME')
GITHUB_OAUTH_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_OAUTH_PERSONAL_ACCESS_TOKEN')

ORCID_CLIENT_ID = os.getenv('ORCID_CLIENT_ID')
ORCID_CLIENT_SECRET = os.getenv('ORCID_CLIENT_SECRET')

# DATABASE CONFIG
DB_DRIVER = os.getenv('DB_DRIVER') or 'pymysql'
DB_TYPE = os.getenv('DB_TYPE') or 'mysql'
DB_HOST = os.getenv('DB_HOST') or 'databse'
DB_PORT = os.getenv('DB_PORT') or '3306'
DB_DATABASE = os.getenv('DB_DATABASE') or 'quickapi'
DB_USERNAME = os.getenv('DB_USERNAME') or 'quickapi'
DB_PASSWORD = os.getenv('DB_PASSWORD') or 'NONE'

SQL_ALCHEMY_URL = DB_TYPE+'+'+DB_DRIVER+'://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_DATABASE