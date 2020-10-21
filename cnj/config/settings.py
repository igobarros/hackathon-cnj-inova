import os

import sqlalchemy as db
from dotenv import load_dotenv, find_dotenv



load_dotenv(find_dotenv())
# load environment variables

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
DB_IP = os.getenv("DB_IP")


def connect_db():
    # create db create_engine
    engine = db.create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_NAME}')
    return engine