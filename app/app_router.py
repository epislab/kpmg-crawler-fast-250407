from fastapi import APIRouter

from app.api.music.melon_router import router as melon_router


router = APIRouter()

router.include_router(melon_router)