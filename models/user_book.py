from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UserBook(Base):
    __tablename__ = "user_books"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(String, default="reading")  # reading, completed, on hold, dropped
    bookmark_page = Column(Integer, default=0)

    user = relationship("User", backref="user_books")
    book = relationship("Book", backref="user_books")
