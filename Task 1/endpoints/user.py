from fastapi import APIRouter

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_user():
    return {"name": "John", "email": "john@example.com"}