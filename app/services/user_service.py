from sqlalchemy.orm import Session
from app.repository import user_repo
from app.core.security import hash_password


def register_user(db: Session, user_input):
    existing_user = user_repo.get_user_by_email(db, user_input.email)

    if existing_user:
        raise Exception("Email already registered")

    user_data = user_input.dict()
    user_data["password_hash"] = hash_password(user_data.pop("password"))

    return user_repo.create_user(db, user_data)