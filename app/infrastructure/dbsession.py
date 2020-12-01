import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQL_ALCHEMY_URL



engine = create_engine(SQL_ALCHEMY_URL)
SessionLocal = sessionmaker(bind=engine)