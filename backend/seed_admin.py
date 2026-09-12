"""
Run this script once to create the default admin account.
Usage: python seed_admin.py
"""
import asyncio
import ssl
import uuid
import os

import asyncpg
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def main():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    conn = await asyncpg.connect(os.getenv("DATABASE_URL"), ssl=ssl_ctx)

    existing = await conn.fetchrow(
        "SELECT id FROM users WHERE email = 'admin@krishisetu.com'"
    )
    if existing:
        print("Admin account already exists.")
        await conn.close()
        return

    password_hash = pwd_context.hash("admin123")

    await conn.execute(
        """INSERT INTO users (id, name, email, phone, password_hash, role)
           VALUES ($1, $2, $3, $4, $5, $6)""",
        uuid.uuid4(),
        "Admin",
        "admin@krishisetu.com",
        "0000000000",
        password_hash,
        "admin",
    )

    print("Admin account created!")
    print("Email: admin@krishisetu.com")
    print("Password: admin123")
    print("WARNING: Change this password after first login!")

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
