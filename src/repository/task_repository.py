from sqlachemy.orm import Session
from src.models import Tasks
from typing import Optional, List


class TaskRespository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def find_all(self) -> List[Tasks]:
        return self.db_session.query(Tasks).all()

    def find_by_user(self, user_id: int) -> List[Tasks]:
        return self.db_session.filter(Tasks.user_id == user_id).all()
    
    def find_by_id(self, task_id: int) -> List[Tasks]:
        return self.db_session.filter(Tasks.id == task_id).first()
    
    def add_task(self, task: Task):
        self.db_session.add(task)
        self.db_session.commit()

    def delete_task(self, task_id: int):
        task = self.db_session.query(Task).filter(Task.id == task_id).first()
        if task:
            self.db_session.delete(task)
            self.db_session.commit()
