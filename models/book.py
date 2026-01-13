from sqlalchemy import Column, Integer, String, Text
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    genre = Column(String)
    book_type = Column(String)
    cover_path = Column(String)
    content_path = Column(String)
    audio_path = Column(String)
