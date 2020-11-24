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
