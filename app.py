import streamlit as st
from database import get_db, engine, Base
from models.user import User
from models.book import Book
from auth import login, register
from admin import admin_panel
import os

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Page setup
st.set_page_config(page_title="OmniLibrary", layout="wide")
st.title("📚 OmniLibrary")

# Initialize session state
if "selected_book_id" not in st.session_state:
    st.session_state.selected_book_id = None

if "page" not in st.session_state:
    st.session_state.page = "browse"

if "user" not in st.session_state:
    st.session_state.user = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Database session
db = get_db()

# ----------------------
# Ensure admin user exists
# ----------------------
admin_user = db.query(User).filter(User.username == "admin").first()
if not admin_user:
    admin_user = User(username="admin")
    admin_user.set_password("admin123")  # Change this password later
    admin_user.is_admin = True
    db.add(admin_user)
    db.commit()
    st.info("Default admin created: username='admin', password='admin123'")

# Sidebar menu
menu = ["Home", "Browse Books", "Login", "Register", "Admin"]
choice = st.sidebar.selectbox("Menu", menu)

# =======================
# Home Page
# =======================
if choice == "Home":
    st.subheader("Welcome to OmniLibrary")
    st.write("Read novels, view manga/manhwa, and listen to audiobooks!")

# =======================
# Browse Books Page
# =======================
elif choice == "Browse Books" and st.session_state.page == "browse":
    tabs = st.tabs(["All", "Manga", "Manhwa", "Novels", "Audiobooks"])
    books = db.query(Book).all()

    def book_card(book, key_prefix):
        col1, col2 = st.columns([1, 3])
        with col1:
            if book.cover_path and os.path.exists(book.cover_path):
                st.image(book.cover_path, width=150)
        with col2:
            st.markdown(f"### {book.title}")
            st.write(f"Author: {book.author}")
            st.write(f"Type: {book.book_type}")
            if st.button("Open", key=f"{key_prefix}_{book.id}"):
                st.session_state.selected_book_id = book.id
                st.session_state.page = "reader"
                st.rerun()

    # All Books
    with tabs[0]:
        for book in books:
            book_card(book, "all")

    # Manga
    with tabs[1]:
        for book in db.query(Book).filter(Book.book_type == "Manga").all():
            book_card(book, "manga")

    # Manhwa
    with tabs[2]:
        for book in db.query(Book).filter(Book.book_type == "Manhwa").all():
            book_card(book, "manhwa")

    # Novels
    with tabs[3]:
        for book in db.query(Book).filter(Book.book_type == "Novel").all():
            book_card(book, "novel")

    # Audiobooks
    with tabs[4]:
        for book in db.query(Book).filter(Book.book_type == "Audiobook").all():
            book_card(book, "audio")

# =======================
# Reader Page
# =======================
elif choice == "Browse Books" and st.session_state.page == "reader":
    book = db.query(Book).filter(
        Book.id == st.session_state.selected_book_id
    ).first()

    if st.button("⬅ Back to Library"):
        st.session_state.page = "browse"
        st.session_state.selected_book_id = None
        st.rerun()

    st.header(book.title)
    st.caption(f"{book.author} • {book.book_type}")
    st.divider()

    if book.book_type in ["Manga", "Manhwa"]:
        from utils.manga_reader import manga_reader
        manga_reader(book.content_path)

    elif book.book_type == "Novel":
        if os.path.exists(book.content_path):
            with open(book.content_path, "r", encoding="utf-8") as f:
                st.text(f.read())

    elif book.book_type == "Audiobook":
        if os.path.exists(book.audio_path):
            st.audio(book.audio_path)

# =======================
# Login Page
# =======================
elif choice == "Login":
    login()

# =======================
# Register Page
# =======================
elif choice == "Register":
    register()

# =======================
# Admin Page
# =======================
elif choice == "Admin":
    if not st.session_state.get("is_admin"):
        st.warning("⚠ You must be logged in as an admin to access this page.")
        login()
    else:
        admin_panel()
