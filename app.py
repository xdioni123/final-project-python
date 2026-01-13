import streamlit as st
from database import get_db, engine, Base
from models.user import User
from models.book import Book
from auth import login, register
from admin import admin_panel
from PIL import Image
import os

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

st.title("OmniLibrary")

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
            st.write(f"**{book.title}** by {book.author}")
            if book.book_type in ["Manga", "Manhwa"] and book.cover_path:
                if os.path.exists(book.cover_path):
                    st.image(book.cover_path, use_column_width=True)
            elif book.book_type == "Novel" and book.content_path:
                if os.path.exists(book.content_path):
                    with open(book.content_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.text_area(book.title, content, height=400)
            elif book.book_type == "Audiobook" and book.audio_path:
                if os.path.exists(book.audio_path):
                    st.audio(book.audio_path)


    with tabs[1]:
        st.subheader("Manga")
        mangas = db.query(Book).filter(Book.book_type=="Manga").all()
        for book in mangas:
            st.write(f"**{book.title}** by {book.author}")
            if book.cover_path and os.path.exists(book.cover_path):
                st.image(book.cover_path, use_column_width=True)

    with tabs[2]:
        st.subheader("Manhwa")
        manhwas = db.query(Book).filter(Book.book_type=="Manhwa").all()
        for book in manhwas:
            st.write(f"**{book.title}** by {book.author}")
            if book.cover_path and os.path.exists(book.cover_path):
                st.image(book.cover_path, use_column_width=True)


    with tabs[3]:
        st.subheader("Novels")
        novels = db.query(Book).filter(Book.book_type=="Novel").all()
        for book in novels:
            st.write(f"**{book.title}** by {book.author}")
            if book.content_path and os.path.exists(book.content_path):
                with open(book.content_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.text_area(book.title, content, height=400)


    with tabs[4]:
        st.subheader("Audiobooks")
        audios = db.query(Book).filter(Book.book_type=="Audiobook").all()
        for book in audios:
            st.write(f"**{book.title}** by {book.author}")
            if book.audio_path and os.path.exists(book.audio_path):
                st.audio(book.audio_path)

elif choice == "Login":
    login()

elif choice == "Register":
    register()

elif choice == "Admin":
    admin_panel()
