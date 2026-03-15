import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import hash_password
from app.core import config
from uuid import uuid4
from datetime import datetime, timezone

from app.core.database import SessionLocal

from app.models.user import User


def create_admin(db=None):
    """
    Create SUPER_ADMIN user if not exists.
    Reads credentials from environment variables.
    
    Args:
        db: Optional database session. Creates new if not provided.
        
    Returns:
        User object if created, None if already exists
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    
    try:
        # Check if admin already exists
        existing = db.query(User).filter(User.role == "SUPER_ADMIN").first()
        if existing:
            print("SUPER_ADMIN already exists.")
            return None

        admin = User(
            id=uuid4(),
            first_name=config.SUPER_ADMIN_FIRST_NAME,
            last_name=config.SUPER_ADMIN_LAST_NAME,
            email=config.SUPER_ADMIN_EMAIL,
            username=config.SUPER_ADMIN_USERNAME,
            mobile=config.SUPER_ADMIN_MOBILE or None,
            password_hash=hash_password(config.SUPER_ADMIN_PASSWORD),
            role="SUPER_ADMIN",
            created_at=datetime.now(timezone.utc)
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("SUPER_ADMIN created successfully!")
        print(f"Email: {config.SUPER_ADMIN_EMAIL}")
        print(f"Password: {config.SUPER_ADMIN_PASSWORD}")
        
        return admin
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    create_admin()