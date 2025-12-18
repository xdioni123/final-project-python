# app.py
import streamlit as st
from database import db
from models.book import Book

st.title("OmniLibrary")

menu = ["Home", "Browse Books", "Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to OmniLibrary")
    st.write("Discover novels, manga, manhwa, and audiobooks!")

elif choice == "Browse Books":
    books = Book.query.all()
    for book in books:
        st.write(f"**{book.title}** by {book.author}")
        if book.cover_image:
            st.image(book.cover_image, width=150)
        if book.book_type == "Audiobook" and book.audio_path:
            st.audio(book.audio_path)
        if book.content_path:
            st.write(f"[Read Book]({book.content_path})")
