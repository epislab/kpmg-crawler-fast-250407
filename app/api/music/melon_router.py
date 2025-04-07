from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, APIRouter, Body, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from typing import Annotated
from fastapi.responses import JSONResponse

from app.domain.music.controllers.melon_controller import MelonController
import logging

logging.basicConfig(level=logging.INFO)



router = APIRouter(prefix="/melon", tags=["melon"])
controller = MelonController()



@router.get("/top100")
async def handle_music():
    logging.info("🔑🔑🔑🔑🔑🔑멜론 차트 크롤링 시작")

    return await controller.get_top100()

