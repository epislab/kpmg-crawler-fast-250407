from fastapi import APIRouter

from app.domain.music.controllers.melon_controller import MelonController
import logging

logging.basicConfig(level=logging.INFO)



router = APIRouter(prefix="/melon", tags=["melon"])
controller = MelonController()



@router.get("/top100")
async def handle_music():
    logging.info("🔑🔑🔑🔑🔑🔑멜론 차트 크롤링 시작")

    return await controller.get_top100()

