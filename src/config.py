from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent


# Actually I use postgresql in production, but in tz sayed sqlite3
DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}/database.db"

# Test
DATABASE_URL_TEST = f"sqlite+aiosqlite:///{BASE_DIR}/test.db"

SECRET = env.str("SECRET")

BILLZ_SECRET_KEY = env.str("BILLZ_SECRET_KEY")
BILLZ_API_KEY = env.str("BILLZ_API_KEY")

FRONTEND_BASE_URL = env.str("FRONTEND_BASE_URL")


db: int = env.int('REDIS_DATABASE') if env.str('REDIS_DATABASE') else None
""" Redis Database ID """
host: str = env.str('REDIS_HOST', None)
port: int = env.int('REDIS_PORT', 6379)
passwd: str | None = env.str('REDIS_PASSWORD', None)
username: str | None = env.str('REDIS_USERNAME', None)
state_ttl: int | None = env.int('REDIS_TTL_STATE', None)
data_ttl: int | None = env.int('REDIS_TTL_DATA', None)

