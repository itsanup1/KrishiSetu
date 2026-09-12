from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from app.dependencies.auth import require_role
from app.database import get_pool

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
async def list_users(user: dict = Depends(require_role("admin"))):
    pool = get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT id, name, email, phone, role, location, is_active, created_at
               FROM users ORDER BY created_at DESC"""
        )
    return [dict(row) for row in rows]
