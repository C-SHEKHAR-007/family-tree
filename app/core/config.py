import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

DATABASE_URL = os.getenv("DATABASE_URL")
# Separate DB for tests; fallback to DATABASE_URL when not set (e.g. local dev)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")

# Super Admin Configuration
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")
SUPER_ADMIN_FIRST_NAME = os.getenv("SUPER_ADMIN_FIRST_NAME")
SUPER_ADMIN_LAST_NAME = os.getenv("SUPER_ADMIN_LAST_NAME")
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME")
SUPER_ADMIN_MOBILE = os.getenv("SUPER_ADMIN_MOBILE")