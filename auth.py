import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/auth"


def login():
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{API_URL}/login",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            data = res.json()
            st.session_state.user = data["username"]
            st.session_state.is_admin = data["is_admin"]
            st.success("Logged in!")
            st.rerun()
        else:
            st.error(res.json()["detail"])


def register():
    st.subheader("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            st.success("Account created! You can now log in.")
        else:
            st.error(res.json()["detail"])
