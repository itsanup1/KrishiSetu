import ssl
import asyncpg
from app.config import DATABASE_URL

pool = None


async def connect_db():
    global pool
    # Supabase requires SSL for external connections
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    pool = await asyncpg.create_pool(dsn=DATABASE_URL, ssl=ssl_ctx)


async def disconnect_db():
    global pool
    if pool:
        await pool.close()


def get_pool():
    return pool
