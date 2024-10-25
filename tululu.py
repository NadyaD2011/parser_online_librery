import requests
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse
import argparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(response, filename, book_id, folder="books/"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{book_id}.{filename}.txt"
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
    comments = []
    genres = []
    
    title, author = soup.select_one("body div[id=content] h1").text.split(
        " \xa0 :: \xa0 "
    )
    title = sanitize_filename(title)

    img = soup.find("div", class_="bookimage").find("a").find("img")["src"]

    all_comments = soup.find_all("div", class_="texts")
    for comment in all_comments:
        comments.append(comment.find("span").text)

    genres_site = soup.find("span", class_="d_book").find_all("a")
    for genre in genres_site:
        genres.append(genre.text)

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
        url_book_site = f"https://tululu.org/b{book_id}/"
        params = {"id": book_id}      
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            check_for_redirect(response)

            page_response = requests.get(url_book_site)
            page_response.raise_for_status()
            check_for_redirect(page_response)

            book_data = parse_book_page(page_response)

            download_txt(response, book_data["title"], book_id)
            download_image(book_data["cover_path"], url_book_site)

        except requests.HTTPError:
            print("Книга не найдена")
        except requests.ConnectionError:
            print("Произошла ошибка подключения.")


if "__main__" == __name__:
    main()
