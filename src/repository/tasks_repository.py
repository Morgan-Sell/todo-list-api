from typing import List, Optional

from sqlalchemy.orm import Session

from src.models import Tasks


class TasksRespository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_all_tasks(self) -> List[Tasks]:
        return self.db_session.query(Tasks).all()

    def find_tasks_by_user(self, user_id: int) -> List[Tasks]:
        return (
            self.db_session.query(Tasks)
            .filter_by(user_id=user_id)
            .order_by(Tasks.id)
            .all()
        )

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

    def edit_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        task = self.find_task_by_id(task_id)

        # Check if task exists
        if task is not None:
            if title is not None and title.strip() != "":
                task.title = title

            if description is not None and description.strip() != "":
                task.description = description

            if status is not None and status.strip() != "":
                task.status = status

            # if none of the variables are none, then commit changes
            if title or description or status:
                self.db_session.commit()
