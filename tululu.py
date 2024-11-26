import requests
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse
import argparse
import time


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(response, filename, folder="books/"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{filename}.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as file:
        file.write(response.content)


def download_image(img, book_url, folder="images/"):
    os.makedirs(folder, exist_ok=True)
    filename = urlparse(img)
    filename = os.path.basename(filename.path)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)

    img_url = urljoin(book_url, img)
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)

    with open(filepath, "wb") as file:
        file.write(response.content)


def parse_book_page(page_response):
    soup = BeautifulSoup(page_response.text, "lxml")

    title, author = soup.select_one("body div[id=content] h1").text.split(
        " \xa0 :: \xa0 "
    )
    title = sanitize_filename(title)

    img = soup.find("div", class_="bookimage").find("a").find("img")["src"]

    all_comments = soup.find_all("div", class_="texts")
    comments = [comment.find("span").text for comment in all_comments]

    genres_site = soup.find("span", class_="d_book").find_all("a")
    genres = [genre.text for genre in genres_site]

    book_data = {
        "author": author,
        "title": title,
        "cover_path": img,
        "comments": comments,
        "genres": genres,
    }

    return book_data


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
        book_site_url = f"https://tululu.org/b{book_id}/"
        params = {"id": book_id}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            check_for_redirect(response)

            page_response = requests.get(book_site_url)
            page_response.raise_for_status()
            check_for_redirect(page_response)

            book_elements = parse_book_page(page_response)

            download_txt(response, book_elements["title"])
            download_image(book_elements["cover_path"], book_site_url)

        except requests.HTTPError:
            print("Книга не найдена")
        except requests.ConnectionError:
            print("Произошла ошибка подключения.")
            time.sleep(3)


if "__main__" == __name__:
    main()
