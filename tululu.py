import requests
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse
import argparse


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()

    if response.content:
        return response


def download_txt(url, filename, book_id, folder="books/"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{book_id}.{filename}.txt"
    response = get_response(url)
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as file:
        file.write(response.content)


def download_image(img, folder="images/"):
    os.makedirs(folder, exist_ok=True)
    filename = urlparse(img)
    filename = os.path.basename(filename.path)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)

    response = get_response(img)
    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(response.content)


def parse_book_page(book_page, book_url):
    try:
        soup = BeautifulSoup(book_page, "lxml")
        comments = []
        genres = []

        href = soup.select_one(".d_book a[title*='скачать книгу txt']")["href"]

        if not href:
            raise Exception

        title, author = soup.select_one("body div[id=content] h1").text.split(
            " \xa0 :: \xa0 "
        )
        title = sanitize_filename(title)

        img = soup.find("div", class_="bookimage").find("a").find("img")["src"]
        cover_path = urljoin(book_url, img)

        all_comments = soup.find_all("div", class_="texts")
        for comment in all_comments:
            comments.append(comment.find("span").text)

        genres_site = soup.find("span", class_="d_book").find_all("a")
        for genre in genres_site:
            genres.append(genre.text)

        book_data = {
            "author": author,
            "title": title,
            "cover_path": cover_path,
            "comments": comments,
            "genres": genres,
        }

        return book_data

    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Программа скачивает книги с сайта tululu.org и достаёт данные о книге"
    )
    parser.add_argument(
        "-start", "--start_id", help="Первая книганужная вам", default=1, type=int
    )
    parser.add_argument(
        "-end", "--end_id", help="Последняя книга нужная вам", default=10, type=int
    )
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id):
        url = "https://tululu.org/txt.php"
        url_book_site = f"https://tululu.org/b{book_id}"
        params = {'id': book_id}
        book_page = requests.get(url_book_site, params=params)
        book_page.raise_for_status()
        book_page = book_page.text
        book_data = parse_book_page(book_page, url_book_site)
        if book_data is None:
            continue
        elif book_data is None:
            continue
        else:
            download_txt(url, book_data["title"], book_id)
            download_image(book_data["cover_path"])


if "__main__" == __name__:
    main()
