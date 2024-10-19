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


def get_name_book(url_book):
    try:
        response = get_response(url_book)
        soup = BeautifulSoup(response.text, "lxml")
        href = soup.select_one(".d_book a[title*='скачать книгу txt']")["href"]

        if not href:
            raise Exception

        content_text, content_auhtor = soup.select_one(
            "body div[id=content] h1"
        ).text.split(" :: ")
        content_text = content_text.strip("\xa0").strip(" ")

        return content_text

    except Exception:
        pass


def get_img_book(url_book):
    try:
        response = get_response(url_book)
        soup = BeautifulSoup(response.text, "lxml")
        img = soup.find("div", class_="bookimage").find("a").find("img")["src"]
        url_book = urljoin(url_book, img)
        return url_book

    except Exception:
        pass


def download_txt(url, filename, book_id, folder="books/"):
    create_path(folder)
    filename = f"{book_id+1}.{filename}.txt"
    response = get_response(url)
    filename = sanitize_filename(filename)
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


def get_comments(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    comments = soup.find_all("div", class_="texts")
    for comment in comments:
        comment = comment.find("span")
        comment = comment.text

        return comment


def get_genre_book(url):
    genres = []
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    genres_site = soup.find("span", class_="d_book").find_all('a')
    for genre in genres_site:
        genre = genre.text
        genres.append(genre)
    print(genres)    

    return genres


def main():
    for book_id in range(10):
        url = f"https://tululu.org/txt.php?id={book_id+1}"
        url_book_site = f"https://tululu.org/b{book_id+1}"
        filename = get_name_book(url_book_site)
        img = get_img_book(url_book_site)
        if filename is None:
            continue
        else:
            # download_txt(url, filename, book_id)
            # download_image(img)
            # get_comments(url_book_site)
            get_genre_book(url_book_site)


if "__main__" == __name__:
    main()
