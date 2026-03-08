import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import hash_password
from uuid import uuid4
from datetime import datetime, timezone

from app.core.database import SessionLocal

from app.models.user import User
from app.models.person import Person

def create_admin():
    db = SessionLocal()

    # Check if admin already exists
    existing = db.query(User).filter(User.role == "SUPER_ADMIN").first()
    if existing:
        print("SUPER_ADMIN already exists.")
        return

    admin = User(
        id=uuid4(),
        first_name="Super",
        last_name="Admin",
        email="c.shekhar.c101@gmail.com",
        username="superadmin",
        mobile="9807084494",
        password_hash=hash_password("Admin@123"),
        role="SUPER_ADMIN",
        created_at=datetime.now(timezone.utc)
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("SUPER_ADMIN created successfully!")
    print("Email: c.shekhar.c101@gmail.com")
    print("Password: Admin@123")


if __name__ == "__main__":
    create_admin()