from fastapi import APIRouter
from endpoints import product, user

router = APIRouter()
router.include_router(product.router)
router.include_router(user.router)