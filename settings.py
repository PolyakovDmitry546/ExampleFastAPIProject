from pathlib import Path

BASE_DIR = Path(__file__).parent

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DB_URL = f'sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3'

TOKEN_URL = 'auth/login'
