from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime

from app.domain.music.models.song import Song

class SongRepository(ABC):
    """노래 데이터 저장소 인터페이스"""
    
    @abstractmethod
    def save_songs(self, songs: List[Song], date: datetime) -> bool:
        """노래 목록을 저장합니다."""
        pass
    
    @abstractmethod
    def get_songs_by_date(self, date: datetime) -> List[Dict]:
        """특정 날짜의 노래 목록을 조회합니다."""
        pass
    
    @abstractmethod
    def get_latest_songs(self) -> List[Dict]:
        """가장 최근의 노래 목록을 조회합니다."""
        pass

class InMemorySongRepository(SongRepository):
    """메모리 기반 노래 저장소 구현체"""
    
    def __init__(self):
        self._storage: Dict[str, List[Dict]] = {}
    
    def save_songs(self, songs: List[Song], date: datetime) -> bool:
        """노래 목록을 메모리에 저장합니다."""
        date_str = date.strftime("%Y-%m-%d")
        self._storage[date_str] = [
            {
                "rank": song.rank,
                "title": song.title,
                "artist": song.artist
            }
            for song in songs
        ]
        return True
    
    def get_songs_by_date(self, date: datetime) -> List[Dict]:
        """특정 날짜의 노래 목록을 조회합니다."""
        date_str = date.strftime("%Y-%m-%d")
        return self._storage.get(date_str, [])
    
    def get_latest_songs(self) -> List[Dict]:
        """가장 최근의 노래 목록을 조회합니다."""
        if not self._storage:
            return []
        
        latest_date = max(self._storage.keys())
        return self._storage[latest_date] 