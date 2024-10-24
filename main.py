import requests
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()

    if response.content:
        return response


def create_path(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_txt(url, filename, book_id, folder="books/"):
    create_path(folder)
    filename = f"{book_id+1}.{filename}.txt"
    response = get_response(url)
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as file:
        file.write(response.content)


def download_image(img, folder="images/"):
    create_path(folder)
    filename = urlparse(img)
    filename = os.path.basename(filename.path)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)

    response = get_response(img)
    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(response.content)


def parse_book_page(book_page, url_book):
    try:
        soup = BeautifulSoup(book_page, "lxml")
        comments = []
        genres = []
        book_info = {}

        title, author = soup.select_one("body div[id=content] h1").text.split(
            " \xa0 :: \xa0 "
        )
        title = sanitize_filename(title)
        book_info["author"] = author
        book_info["title"] = title

        img = soup.find("div", class_="bookimage").find("a").find("img")["src"]
        cover_path = urljoin(url_book, img)
        book_info["cover_path"] = cover_path

        all_comments = soup.find_all("div", class_="texts")
        for comment in all_comments:
            comments.append(comment.find("span").text)
        book_info["comments"] = comments

        genres_site = soup.find("span", class_="d_book").find_all("a")
        for genre in genres_site:
            genres.append(genre.text)
        book_info["genres"] = genres

        return book_info

    except Exception:
        pass


def main():
    for book_id in range(10):
        url = f"https://tululu.org/txt.php?id={book_id+1}"
        url_book_site = f"https://tululu.org/b{book_id+1}"
        book_page = requests.get(url_book_site)
        book_page.raise_for_status()
        book_page = book_page.text
        book_info = parse_book_page(book_page, url_book_site)
        if book_info is None:
            continue
        elif book_info is None:
            continue
        else:
            download_txt(url, book_info['title'], book_id)
            download_image(book_info['cover_path'])


if "__main__" == __name__:
    main()
