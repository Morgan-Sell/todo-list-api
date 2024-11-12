from typing import List, Optional

from sqlalchemy.orm import Session

from src.models import Users
from src.security import check_password_hash, generate_password_hash


class UsersRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_all_users(self) -> List[Users]:
        return self.db_session.query(Users).all()

    def find_user_by_id(self, user_id: int) -> Optional[Users]:
        return self.db_session.query(Users).filter_by(id=user_id).first()

    def find_user_by_username(self, username: str) -> Optional[Users]:
        return self.db_session.query(Users).filter_by(username=username).first()

    def get_user_password(self, username: str) -> Optional[str]:
        user = self.db_session.query(Users).filter_by(username=username).first()
        return user.password_hash if user is not None else None

    def change_user_password(self, username: str, new_password) -> bool:
        user = self.find_user_by_username(username=username)

        if user is not None:
            user.password_hash = generate_password_hash(new_password)
            self.db_session.commit()
            return True
        return False

    def add_user(self, username: str, password) -> bool:
        # check if user already exists
        if self.find_user_by_username(username=username) is not None:
            return False

        hashed_password = generate_password_hash(password)
        new_user = Users(username=username, password_hash=hashed_password)
        self.db_session.add(new_user)
        self.db_session.commit()

    def delete_user(self, username: str, password: str) -> bool:
        user = self.db_session.query(Users).filter_by(username=username).first()

        if user is not None and check_password_hash(user.password_hash, password):
            self.db_session.delete(user)
            self.db_session.commit()
            return True
        return False
