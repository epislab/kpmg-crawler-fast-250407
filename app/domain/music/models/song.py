from dataclasses import dataclass

@dataclass
class Song:
    """멜론 차트 노래 정보 모델"""
    rank: int
    title: str
    artist: str 