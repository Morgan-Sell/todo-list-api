from sqlalchemy.orm import Session
from src.models import Users, Tasks


def create_task(db: Session, title: str, description: str, user_id: int):
    new_task = Tasks(title=title, description=description, user_id=user_id)
    db.add(new_task)
    db.commit()