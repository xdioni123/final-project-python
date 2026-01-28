import streamlit as st
from database import get_db, engine, Base
from models.user import User
from models.book import Book
from auth import login, register
from admin import admin_panel
import os

# ----------------------
# Database setup
# ----------------------
Base.metadata.create_all(bind=engine)
db = get_db()

# ----------------------
# Page setup
# ----------------------
st.set_page_config(page_title="OmniLibrary", layout="wide")
st.title("📚 OmniLibrary")

# ----------------------
# Session state
# ----------------------
if "selected_book_id" not in st.session_state:
    st.session_state.selected_book_id = None

if "page" not in st.session_state:
    st.session_state.page = "browse"

if "user" not in st.session_state:
    st.session_state.user = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ----------------------
# Ensure default admin exists
# ----------------------
admin = db.query(User).filter(User.username == "admin").first()
if not admin:
    admin = User(username="admin")
    admin.set_password("admin123")
    admin.is_admin = True
    db.add(admin)
    db.commit()
    st.info("Default admin created: username='admin', password='admin123'")

# ----------------------
# Sidebar menu
# ----------------------
menu = ["Home", "Browse Books", "Login", "Register", "Admin"]
choice = st.sidebar.selectbox("Menu", menu)

# ----------------------
# Helper: book card
# ----------------------
def book_card(book, key_prefix):
    col1, col2 = st.columns([1, 3])

    # ---- COVER IMAGE ----
    with col1:
        cover_path = book.cover_path
        if cover_path and os.path.exists(cover_path):
            st.image(cover_path, width=150)
        else:
            st.image("assets/no_cover.png", width=150)

    # ---- INFO ----
    with col2:
        st.markdown(f"### {book.title}")
        st.write(f"Author: {book.author}")
        st.write(f"Type: {book.book_type}")

        if st.button("Open", key=f"{key_prefix}_{book.id}"):
            st.session_state.selected_book_id = book.id
            st.session_state.page = "reader"
            st.rerun()

# =======================
# HOME
# =======================
if choice == "Home":
    st.subheader("Welcome to OmniLibrary")
    st.write("Read novels, manga, manhwa, and listen to audiobooks!")

# =======================
# BROWSE BOOKS
# =======================
elif choice == "Browse Books" and st.session_state.page == "browse":
    tabs = st.tabs(["All", "Manga", "Manhwa", "Novels", "Audiobooks"])

    with tabs[0]:
        for book in db.query(Book).all():
            book_card(book, "all")

    with tabs[1]:
        for book in db.query(Book).filter(Book.book_type == "Manga").all():
            book_card(book, "manga")

    with tabs[2]:
        for book in db.query(Book).filter(Book.book_type == "Manhwa").all():
            book_card(book, "manhwa")

    with tabs[3]:
        for book in db.query(Book).filter(Book.book_type == "Novel").all():
            book_card(book, "novel")

    with tabs[4]:
        for book in db.query(Book).filter(Book.book_type == "Audiobook").all():
            book_card(book, "audio")

# =======================
# READER PAGE
# =======================
elif choice == "Browse Books" and st.session_state.page == "reader":
    book = db.query(Book).filter(
        Book.id == st.session_state.selected_book_id
    ).first()

    if st.button("⬅ Back to Library"):
        st.session_state.page = "browse"
        st.session_state.selected_book_id = None
        st.rerun()

    # Show cover
    if book.cover_path and os.path.exists(book.cover_path):
        st.image(book.cover_path, width=250)
    else:
        st.image("assets/no_cover.png", width=250)

    st.header(book.title)
    st.caption(f"{book.author} • {book.book_type}")
    st.divider()

    # Manga / Manhwa reader
    if book.book_type in ["Manga", "Manhwa"]:
        from utils.manga_reader import manga_reader
        manga_reader(book.content_path)

    # Novel reader
    elif book.book_type == "Novel":
        if book.content_path and os.path.exists(book.content_path):
            with open(book.content_path, "r", encoding="utf-8") as f:
                st.text(f.read())

        # Optional audiobook for novels
        if book.audio_path and os.path.exists(book.audio_path):
            st.audio(book.audio_path)

    # Audiobooks
    elif book.book_type == "Audiobook":
        if book.audio_path and os.path.exists(book.audio_path):
            st.audio(book.audio_path)

# =======================
# LOGIN / REGISTER
# =======================
elif choice == "Login":
    login()

elif choice == "Register":
    register()

# =======================
# ADMIN
# =======================
elif choice == "Admin":
    if not st.session_state.is_admin:
        st.warning("Admin access required")
        login()
    else:
        admin_panel()
