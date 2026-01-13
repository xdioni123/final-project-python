import streamlit as st
from database import get_db
from models.book import Book

def admin_panel():
    if not st.session_state.get("is_admin"):
        st.error("Access denied")
        return

    db = get_db()

    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    book_type = st.selectbox("Type", ["Novel", "Manga", "Manhwa", "Audiobook"])
    cover_path = st.text_input("Cover Path")
    content_path = st.text_input("Content Path")
    audio_path = st.text_input("Audio Path")

    if st.button("Add Book"):
        book = Book(
            title=title,
            author=author,
            genre=genre,
            book_type=book_type,
            cover_path=cover_path,
            content_path=content_path,
            audio_path=audio_path
        )
        db.add(book)
        db.commit()
        st.success("Book added successfully")
