import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from dotenv import load_dotenv

from src.config import DB_HOST, DB_NAME, DB_PORT


load_dotenv()
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{username}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
# Since automcocommit is false, session.commit() is required to edit the database.
# autoflush=False - Requires commit command. Avoid unneccesary write commands
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()
