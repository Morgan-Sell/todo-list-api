from typing import List, Optional

from sqlalchemy.orm import Session

from src.models import Tasks


class TasksRespository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_all_tasks(self) -> List[Tasks]:
        return self.db_session.query(Tasks).all()

    def find_tasks_by_user(self, user_id: int) -> List[Tasks]:
        return self.db_session.query(Tasks).filter_by(user_id=user_id).all()

    def find_task_by_id(self, task_id: int) -> Optional[Tasks]:
        return self.db_session.query(Tasks).filter_by(id=task_id).first()

    def add_task(self, task: Tasks):
        self.db_session.add(task)
        self.db_session.commit()

    def delete_task(self, task_id: int):
        task = self.find_task_by_id(task_id)
        if task is not None:
            self.db_session.delete(task)
            self.db_session.commit()
