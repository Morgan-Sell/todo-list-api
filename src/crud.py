from sqlalchemy.orm import Session

from src.models import Tasks, Users


def create_user(db: Session, username: str, password_hash: str):
    new_user = Users(username=username, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def create_task(db: Session, title: str, description: str, user_id: int):
    new_task = Tasks(title=title, description=description, user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)


def get_tasks_by_user_id(db: Session, user_id: int):
    return db.query(Tasks).filter(Tasks.user_id == user_id).all()
