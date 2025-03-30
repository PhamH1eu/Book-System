from app.configs.Database import get_session
from fastapi import Depends
from app.models.UserModel import UserInDB
from sqlmodel import Session, select


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_session)) -> None:
        self.db = db

    def get(self, id: int) -> UserInDB:
        return self.db.get(UserInDB, id)

    def getByUsername(self, username: str) -> UserInDB:
        return self.db.exec(
            select(UserInDB).where(UserInDB.username == username)
        ).first()

    def create(self, UserInDB: UserInDB) -> UserInDB:
        self.db.add(UserInDB)
        self.db.commit()
        self.db.refresh(UserInDB)
        return UserInDB

    def delete(self, UserInDB: UserInDB) -> None:
        self.db.delete(UserInDB)
        self.db.commit()
