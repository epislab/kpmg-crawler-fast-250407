from datetime import datetime
from typing import Dict

from app.domain.music.services.melon_service import MelonService

class MelonController:
    """멜론 차트 크롤링 컨트롤러"""
    
    def __init__(self):
        self.service = MelonService()
    
    async def get_top100(self) -> Dict:
        """멜론 차트 TOP100을 크롤링하고 결과를 반환합니다."""
        try:
            songs = await self.service.crawl_top100()
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "total": len(songs),
                "songs": [
                    {
                        "rank": song.rank,
                        "title": song.title,
                        "artist": song.artist
                    }
                    for song in songs
                ]
            }
        except Exception as e:
            return {
                "error": str(e),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "total": 0,
                "songs": []
            }
    
    async def get_latest_songs(self) -> Dict:
        """가장 최근에 크롤링한 노래 목록을 반환합니다."""
        songs = await self.service.get_latest_songs()
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total": len(songs),
            "songs": songs
        }
    
    async def get_songs_by_date(self, date: datetime) -> Dict:
        """특정 날짜의 노래 목록을 반환합니다."""
        songs = self.service.get_songs_by_date(date)
        return {
            "date": date.strftime("%Y-%m-%d"),
            "total": len(songs),
            "songs": songs
        } 


