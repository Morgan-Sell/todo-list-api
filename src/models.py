import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from dotenv import load_dotenv

from src.config import DB_HOST, DB_NAME, DB_PORT, TaskStatus


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



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # tasks is not a column. Enables access at the ORM level.
    tasks = relationship("Tasks", back_populates="owner")


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.NOT_STARTED, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Owners is not a column. 
    owners = relationship("Users", back_populates="tasks")

    
