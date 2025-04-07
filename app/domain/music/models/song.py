from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Song(Base):
    """멜론 차트 노래 정보 모델"""
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        return f"<Song(rank={self.rank}, title='{self.title}', artist='{self.artist}')>" 