import streamlit as st
from database import get_db
from models.book import Book
from models.user import User

def admin_panel():
    if not st.session_state.get("is_admin"):
        st.error("🚫 Access denied. Admins only.")
        return

    db = get_db()
    st.title("🛠 Admin Panel")

    tabs = st.tabs(["📚 Manage Books", "👤 Manage Users"])
    with tabs[0]:
        st.subheader("➕ Add New Book")

        title = st.text_input("Title", key="add_title")
        author = st.text_input("Author", key="add_author")
        genre = st.text_input("Genre", key="add_genre")
        book_type = st.selectbox(
            "Type", ["Novel", "Manga", "Manhwa"], key="add_type"
        )
        cover_path = st.text_input("Cover Path", key="add_cover")
        content_path = st.text_input("Content Path", key="add_content")
        audio_path = st.text_input("Audio Path", key="add_audio")

        if st.button("➕ Add Book"):
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
        if not books:
            st.info("No books found.")
        else:
            book_to_edit = st.selectbox(
                "Select a book",
                books,
                format_func=lambda b: f"{b.title} ({b.book_type})",
                key="edit_select"
            )

            book = db.query(Book).filter(Book.id == book_to_edit.id).first()

            new_title = st.text_input("Title", book.title)
            new_author = st.text_input("Author", book.author)
            new_genre = st.text_input("Genre", book.genre)
            new_book_type = st.selectbox(
                "Type",
                ["Novel", "Manga", "Manhwa"],
                index=["Novel", "Manga", "Manhwa"].index(book.book_type)
            )
            new_cover = st.text_input("Cover Path", book.cover_path or "")
            new_content = st.text_input("Content Path", book.content_path or "")
            new_audio = st.text_input("Audio Path", book.audio_path or "")

            if st.button("💾 Save Changes"):
                book.title = new_title
                book.author = new_author
                book.genre = new_genre
                book.book_type = new_book_type
                book.cover_path = new_cover
                book.content_path = new_content
                book.audio_path = new_audio

                db.commit()
                st.success("Book updated successfully")
                st.rerun()

        st.divider()

        st.subheader("🗑 Delete Book")

        if books:
            book_to_delete = st.selectbox(
                "Select book to delete",
                books,
                format_func=lambda b: f"{b.title} ({b.book_type})",
                key="delete_select"
            )

            if st.button("🗑 Confirm Delete"):
                book = db.query(Book).filter(Book.id == book_to_delete.id).first()
                if book:
                    db.delete(book)
                    db.commit()
                    st.success("Book deleted")
                    st.rerun()

    # =========================
    # 👤 USER MANAGEMENT
    # =========================
    with tabs[1]:
        st.subheader("👤 Manage Users")

        users = db.query(User).all()
        if not users:
            st.info("No users found.")
            return

        selected_user = st.selectbox(
            "Select user",
            users,
            format_func=lambda u: u.username
        )

        user = db.query(User).filter(User.id == selected_user.id).first()

        st.write(f"**Username:** {user.username}")
        st.write(f"**Current role:** {'Admin' if user.is_admin else 'User'}")

        make_admin = st.checkbox("Grant admin privileges", value=user.is_admin)

        if st.button("💾 Save User Changes"):
            user.is_admin = make_admin
            db.commit()
            st.success("User permissions updated")
            st.rerun()
