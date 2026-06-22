import os
import secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    STL_UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads" / "stl"
    PHOTO_UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads" / "photos"
