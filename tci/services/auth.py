from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from tci.core.config import settings
from tci.db.models import User
from tci.db.postgresql import db


class AuthService:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def get_password_hash(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        with db.get_session() as session:
            user = session.query(User).filter(User.email == email).first()
            if user and self.verify_password(password, user.hashed_password):
                return user
        return None

    def create_access_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        to_encode = {"user_id": user_id, "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

    def verify_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            with db.get_session() as session:
                return session.query(User).get(payload["user_id"])
        except JWTError:
            return None

    def register_user(self, email: str, password: str, full_name: str = None) -> User:
        with db.get_session() as session:
            user = User(
                email=email,
                hashed_password=self.get_password_hash(password),
                full_name=full_name,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user


auth_service = AuthService()
