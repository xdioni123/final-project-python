import streamlit as st
import os

def manga_reader(folder_path):
    """Display all images in a folder as manga/manhwa pages."""
    if not os.path.exists(folder_path):
        st.error("Folder not found!")
        return

    # Get all images and sort by filename
    images = sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ])

    if not images:
        st.info("No images found in this folder.")
        return

    # Display images one by one
    for img in images:
        st.image(img, use_container_width=True)

