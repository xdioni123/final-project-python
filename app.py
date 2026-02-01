import streamlit as st
from database import get_db, engine, Base
from models.user import User
from models.book import Book
from auth import login, register
from admin import admin_panel
from models.user_library import UserLibrary
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
admin_user = db.query(User).filter(User.username == "admin").first()
if not admin_user:
    admin_user = User(username="admin")
    admin_user.set_password("admin123")
    admin_user.is_admin = True
    db.add(admin_user)
    db.commit()

# ----------------------
# Sidebar menu (DYNAMIC)
# ----------------------
menu = ["Home", "Browse Books"]

if st.session_state.user is None:
    menu += ["Login", "Register"]
else:
    if st.session_state.is_admin:
        menu.append("Admin")

if "menu_choice" not in st.session_state:
    st.session_state.menu_choice = "Home"

choice = st.sidebar.selectbox(
    "Menu",
    menu,
    index=menu.index(st.session_state.menu_choice)
)


# ----------------------
# Helper: book card
# ----------------------
def book_card(book, key_prefix):
    col1, col2 = st.columns([1, 3])

    with col1:
        if book.cover_path and os.path.exists(book.cover_path):
            st.image(book.cover_path, width=150)
        else:
            st.image("assets/no_cover.png", width=150)

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

    # ---------- HERO ----------
    st.markdown(
        """
        <div style="text-align:center; padding:40px 0;">
            <h1>📚 OmniLibrary</h1>
            <h4 style="color:gray;">
                Read novels, manga, manhwa & listen to audiobooks — all in one place
            </h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- USER SECTION ----------
    if st.session_state.user:
        st.subheader("👋 Welcome back")
        st.write("Continue exploring your library or discover something new.")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📚 Browse Books"):
                st.session_state.page = "browse"
                st.rerun()

        with col_b:
            st.info("📌 Bookmarks & progress coming soon")

    else:
        st.subheader("✨ Get Started")
        st.write("Create an account to track reading progress, rate books, and build your library.")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Login"):
                st.session_state.menu_choice = "Login"
                st.rerun()

        with col_b:
            if st.button("📚 Browse Books"):
                st.session_state.menu_choice = "Browse Books"
                st.session_state.page = "browse"
                st.rerun()


    st.divider()

    # ---------- FEATURED BOOKS ----------
    st.subheader("🔥 Featured Books")

    featured_books = db.query(Book).limit(4).all()

    if not featured_books:
        st.warning("No books available yet.")
    else:
        cols = st.columns(len(featured_books))
        for col, book in zip(cols, featured_books):
            with col:
                if book.cover_path and os.path.exists(book.cover_path):
                    st.image(book.cover_path, use_container_width=True)
                else:
                    st.image("assets/no_cover.png", use_container_width=True)

                st.markdown(f"**{book.title}**")
                st.caption(book.author)

                if st.button("Open", key=f"home_open_{book.id}"):
                    st.session_state.selected_book_id = book.id
                    st.session_state.menu_choice = "Browse Books"
                    st.session_state.page = "reader"
                    st.rerun()


    st.divider()

    # ---------- FOOTER ----------
    st.caption("© OmniLibrary • Read more, discover more 📖")
# =======================
# BROWSE BOOKS
# =======================
elif choice == "Browse Books" and st.session_state.page == "browse":
    tabs = st.tabs(["All", "Manga", "Manhwa", "Novels"])

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

    if book.cover_path and os.path.exists(book.cover_path):
        st.image(book.cover_path, width=250)
    else:
        st.image("assets/no_cover.png", width=250)

    st.header(book.title)
    st.caption(f"{book.author} • {book.book_type}")
    st.divider()

    if book.book_type in ["Manga", "Manhwa"]:
        from utils.manga_reader import manga_reader
        manga_reader(book.content_path)

    elif book.book_type == "Novel":
        if book.content_path and os.path.exists(book.content_path):
            with open(book.content_path, "r", encoding="utf-8") as f:
                st.text(f.read())

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
    admin_panel()
