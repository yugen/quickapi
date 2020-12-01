from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.orm import mapper

from domain.user import User

metadata = MetaData()

user_table = Table(
    'users', 
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String),
    Column('orcid', String)
)

def start_mappers():
    users_mapper = mapper(User, user_table)