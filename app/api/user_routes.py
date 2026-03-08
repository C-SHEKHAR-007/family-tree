from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse
from app.services import user_service
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    try:
        return user_service.register_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

