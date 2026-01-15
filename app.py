import streamlit as st
from database import get_db, engine, Base
from models.user import User
from models.book import Book
from auth import login, register
from admin import admin_panel
import os

Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="OmniLibrary", layout="wide")
st.title("📚 OmniLibrary")

if "selected_book_id" not in st.session_state:
    st.session_state.selected_book_id = None

menu = ["Home", "Browse Books", "Login", "Register", "Admin"]
choice = st.sidebar.selectbox("Menu", menu)

db = get_db()

if choice == "Home":
    st.subheader("Welcome to OmniLibrary")
    st.write("Read novels, view manga/manhwa, and listen to audiobooks!")

elif choice == "Browse Books":
    tabs = st.tabs(["All", "Manga", "Manhwa", "Novels", "Audiobooks"])
    books = db.query(Book).all()

    with tabs[0]:
        st.subheader("All Books")
        for book in books:
            col1, col2 = st.columns([1, 3])

            with col1:
                if book.cover_path and os.path.exists(book.cover_path):
                    st.image(book.cover_path, width=150)

            with col2:
                st.markdown(f"### {book.title}")
                st.write(f"Author: {book.author}")
                st.write(f"Type: {book.book_type}")

                if st.button("Open", key=f"open_{book.id}"):
                    st.session_state.selected_book_id = book.id

    with tabs[1]:
        for book in db.query(Book).filter(Book.book_type == "Manga").all():
            st.write(book.title)
            if st.button("Open", key=f"manga_{book.id}"):
                st.session_state.selected_book_id = book.id

    with tabs[2]:
        for book in db.query(Book).filter(Book.book_type == "Manhwa").all():
            st.write(book.title)
            if st.button("Open", key=f"manhwa_{book.id}"):
                st.session_state.selected_book_id = book.id

    with tabs[3]:
        for book in db.query(Book).filter(Book.book_type == "Novel").all():
            st.write(book.title)
            if st.button("Read", key=f"novel_{book.id}"):
                st.session_state.selected_book_id = book.id

    with tabs[4]:
        for book in db.query(Book).filter(Book.book_type == "Audiobook").all():
            st.write(book.title)
            if st.button("Listen", key=f"audio_{book.id}"):
                st.session_state.selected_book_id = book.id

    if st.session_state.selected_book_id:
        selected_book = db.query(Book).filter(
            Book.id == st.session_state.selected_book_id
        ).first()

        st.divider()
        st.header(selected_book.title)

        if selected_book.book_type in ["Manga", "Manhwa"]:
            from utils.manga_reader import manga_reader
            manga_reader(selected_book.content_path)

        elif selected_book.book_type == "Novel":
            if os.path.exists(selected_book.content_path):
                with open(selected_book.content_path, "r", encoding="utf-8") as f:
                    st.text(f.read())

        elif selected_book.book_type == "Audiobook":
            if os.path.exists(selected_book.audio_path):
                st.audio(selected_book.audio_path)

elif choice == "Login":
    login()

elif choice == "Register":
    register()

elif choice == "Admin":
    admin_panel()
