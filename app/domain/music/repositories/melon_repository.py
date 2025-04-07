from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, delete

from app.domain.music.models.song import Song
from app.foundation.infrastructure.database.database import database

class MelonRepository:
    """멜론 차트 데이터 리포지토리"""
    
    def __init__(self):
        self._db = database
        
    async def save_songs(self, songs: List[Song]) -> None:
        """노래 목록을 데이터베이스에 저장합니다."""
        try:
            async with self._db.session as session:
                async with session.begin():
                    # 기존 데이터 삭제
                    await session.execute(delete(Song))
                    
                    # 새로운 데이터 삽입
                    for song in songs:
                        session.add(song)
                    
                    await session.commit()
        except Exception as e:
            raise Exception(f"데이터베이스 저장 중 오류 발생: {str(e)}")
    
    async def get_latest_songs(self, limit: int = 100) -> List[Song]:
        """가장 최근에 크롤링한 노래 목록을 반환합니다."""
        try:
            async with self._db.session as session:
                result = await session.execute(
                    select(Song)
                    .order_by(desc(Song.created_at))
                    .limit(limit)
                )
                return result.scalars().all()
        except Exception as e:
            raise Exception(f"데이터 조회 중 오류 발생: {str(e)}")
    
    async def get_songs_by_date(self, date: datetime, limit: int = 100) -> List[Song]:
        """특정 날짜의 노래 목록을 반환합니다."""
        try:
            async with self._db.session as session:
                result = await session.execute(
                    select(Song)
                    .where(Song.created_at >= date)
                    .order_by(desc(Song.created_at))
                    .limit(limit)
                )
                return result.scalars().all()
        except Exception as e:
            raise Exception(f"데이터 조회 중 오류 발생: {str(e)}")
