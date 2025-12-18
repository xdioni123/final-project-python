from database import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    book_type = db.Column(db.String(50), nullable=False) 
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(200), nullable=True)
    content_path = db.Column(db.String(200), nullable=True)
    audio_path = db.Column(db.String(200), nullable=True)
