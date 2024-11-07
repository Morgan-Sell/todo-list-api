from typing import List, Optional

from sqlalchemy.orm import Session

from src.models import Users


class UsersRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_all_users(self) -> List[Users]:
        return self.db_session.query(Users).all()

    def find_user_by_id(self, user_id: int) -> Optional[Users]:
        return self.db_session.query(Users).filter_by(id=user_id).first()

    def get_user_password(self, username: str) -> Optional[str]:
        user = self.db_session.query(Users).filter_by(username=username).first()
        return user.password_hash if user is not None else None

    def change_user_password(self, username: str, new_password) -> bool:
        # TODO: must create generate_password_hash() first
        pass

    def add_user(self, user: Users):
        self.db_session.add(user)
        self.db_session.commit()

    def delete_user(self, username: str, password: str) -> bool:
        # TODO: must create authentication to ensure user is deleting themselve
        pass
