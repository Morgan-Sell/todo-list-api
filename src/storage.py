import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

from src.config import DB_HOST, DB_NAME, DB_PORT, DB_USER

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")


def connect_postgres_server():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
