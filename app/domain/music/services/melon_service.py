from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
import aiohttp

from app.domain.music.models.song import Song
from app.domain.music.repositories.melon_repository import InMemorySongRepository

class MelonService:
    def __init__(self):
        self.repository = InMemorySongRepository()
        self.url = "https://smu.melon.com/chart/index.htm#"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.melon.com/chart/index.htm",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.class_name = []

    async def crawl_top100(self) -> List[Song]:
        """멜론 차트 TOP100을 크롤링합니다."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    response.raise_for_status()
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            songs = []
            
            for rank, row in enumerate(soup.select('tbody tr'), 1):
                title = row.select_one('.rank01 span a').text.strip()
                artist = row.select_one('.rank02 span a').text.strip()
                
                song = Song(rank=rank, title=title, artist=artist)
                songs.append(song)
            
            # 크롤링한 데이터를 저장
            self.repository.save_songs(songs, datetime.now())
            
            return songs
            
        except Exception as e:
            raise Exception(f"크롤링 중 오류가 발생했습니다: {str(e)}")
    
    def get_latest_songs(self) -> List[Dict]:
        """가장 최근에 크롤링한 노래 목록을 반환합니다."""
        return self.repository.get_latest_songs()
    
    def get_songs_by_date(self, date: datetime) -> List[Dict]:
        """특정 날짜의 노래 목록을 반환합니다."""
        return self.repository.get_songs_by_date(date) 

