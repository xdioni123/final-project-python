import requests
from bs4 import BeautifulSoup

def scrape_books(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for item in soup.select("article"):
        title = item.find("h2")
        author = item.find("span", class_="author")

        books.append({
            "title": title.text.strip() if title else "Unknown",
            "author": author.text.strip() if author else "Unknown"
        })

    return books
