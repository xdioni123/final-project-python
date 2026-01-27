import streamlit as st
from database import get_db
from models.book import Book
from models.user import User
import os

def admin_panel():
    if not st.session_state.get("is_admin"):
        st.error("🚫 Access denied. Admins only.")
        return

    db = get_db()
    st.title("🛠 Admin Panel")

    tabs = st.tabs(["📚 Manage Books", "👤 Manage Users"])

    # ------------------ BOOK MANAGEMENT ------------------
    with tabs[0]:
        st.subheader("➕ Add New Book")
        title = st.text_input("Title", key="add_title")
        author = st.text_input("Author", key="add_author")
        genre = st.text_input("Genre", key="add_genre")
        book_type = st.selectbox("Type", ["Novel", "Manga", "Manhwa", "Audiobook"], key="add_type")
        cover_path = st.text_input("Cover Path", key="add_cover")
        content_path = st.text_input("Content Path", key="add_content")
        audio_path = st.text_input("Audio Path", key="add_audio")

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
            st.rerun()

        st.divider()
        st.subheader("✏ Edit Book")
        books = db.query(Book).all()
        if books:
            book_to_edit = st.selectbox(
                "Select a book to edit",
                books,
                format_func=lambda b: f"{b.title} ({b.book_type})",
                key="edit_select"
            )
            new_title = st.text_input("Title", book_to_edit.title, key="edit_title")
            new_author = st.text_input("Author", book_to_edit.author, key="edit_author")
            new_genre = st.text_input("Genre", book_to_edit.genre, key="edit_genre")
            new_book_type = st.selectbox(
                "Type",
                ["Novel", "Manga", "Manhwa", "Audiobook"],
                index=["Novel", "Manga", "Manhwa", "Audiobook"].index(book_to_edit.book_type),
                key="edit_type"
            )
            new_cover = st.text_input("Cover Path", book_to_edit.cover_path or "", key="edit_cover")
            new_content = st.text_input("Content Path", book_to_edit.content_path or "", key="edit_content")
            new_audio = st.text_input("Audio Path", book_to_edit.audio_path or "", key="edit_audio")

            if st.button("Save Changes to Book"):
                book_to_edit.title = new_title
                book_to_edit.author = new_author
                book_to_edit.genre = new_genre
                book_to_edit.book_type = new_book_type
                book_to_edit.cover_path = new_cover
                book_to_edit.content_path = new_content
                book_to_edit.audio_path = new_audio
                db.commit()
                st.success("Book updated successfully")
                st.rerun()

        st.divider()
        st.subheader("🗑 Delete Book")
        if books:
            book_to_delete = st.selectbox(
                "Select a book to delete",
                books,
                format_func=lambda b: f"{b.title} ({b.book_type})",
                key="delete_select"
            )
            if st.button("Delete Book"):
                db.delete(book_to_delete)
                db.commit()
                st.success("Book deleted successfully")
                st.rerun()
        else:
            st.info("No books found.")

    # ------------------ USER MANAGEMENT ------------------
    with tabs[1]:
        st.subheader("👤 User Management")
        users = db.query(User).all()

        if not users:
            st.info("No users found.")
            return

        selected_user = st.selectbox(
            "Select user",
            users,
            format_func=lambda u: u.username,
            key="user_select"
        )

        st.write(f"**Username:** {selected_user.username}")
        st.write(f"**Current role:** {'Admin' if selected_user.is_admin else 'User'}")

        make_admin = st.checkbox("Grant admin privileges", value=selected_user.is_admin, key="admin_checkbox")
        if st.button("Save User Changes"):
            selected_user.is_admin = make_admin
            db.commit()
            st.success(f"{selected_user.username}'s permissions updated")
            st.rerun()
