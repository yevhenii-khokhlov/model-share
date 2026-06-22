import os
import secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_secret_key():
    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        return secret_key

    secret_file = BASE_DIR / ".flask_secret"
    if secret_file.exists():
        return secret_file.read_text(encoding="utf-8").strip()

    generated_key = secrets.token_hex(32)
    secret_file.write_text(generated_key, encoding="utf-8")
    return generated_key


class Config:
    SECRET_KEY = load_secret_key()
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    STL_UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads" / "stl"
    PHOTO_UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads" / "photos"
