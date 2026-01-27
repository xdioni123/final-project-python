import streamlit as st
from database import get_db
from models.user import User
from sqlalchemy.exc import IntegrityError


def login():
    db = get_db()

    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = db.query(User).filter(User.username == username).first()

        if user and user.check_password(password):
            st.session_state["user"] = user.username
            st.session_state["is_admin"] = user.is_admin
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid credentials")


def register():
    db = get_db()

    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        try:
            user = User(username=username)
            user.set_password(password)
            db.add(user)
            db.commit()
            st.success("Account created! You can now log in.")
        except IntegrityError:
            db.rollback()
            st.error("Username already exists")