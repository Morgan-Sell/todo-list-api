import os

from dotenv import load_dotenv
from flask_login import UserMixin
from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PORT, TaskStatus

load_dotenv()
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{username}:{password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)
# Since automcocommit is false, session.commit() is required to edit the database.
# autoflush=False - Requires commit command. Avoid unneccesary write commands
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


class Users(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # tasks is not a column. Enables access at the ORM level.
    tasks = relationship("Tasks", back_populates="owners")


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.NOT_STARTED, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Owners is not a column.
    owners = relationship("Users", back_populates="tasks")
