from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth import decode_access_token
from db.database import get_db
from db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Неверный токен")
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
