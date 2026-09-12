import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister, UserLogin, UserOut, Token
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_token
from app.database import get_pool

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserRegister):
    if data.role not in ("farmer", "vendor"):
        raise HTTPException(status_code=400, detail="Role must be 'farmer' or 'vendor'")

    pool = get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT id FROM users WHERE email = $1", data.email
        )
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_id = uuid.uuid4()
        hashed = hash_password(data.password)

        await conn.execute(
            """INSERT INTO users (id, name, email, phone, password_hash, role, location)
               VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            user_id,
            data.name,
            data.email,
            data.phone,
            hashed,
            data.role,
            data.location,
        )

        user = await conn.fetchrow(
            """SELECT id, name, email, phone, role, location, is_active, created_at
               FROM users WHERE id = $1""",
            user_id,
        )

    return dict(user)


@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    pool = get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1", data.email
        )

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_token({"sub": str(user["id"]), "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
