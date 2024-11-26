import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import time
from tululu import *
import json
import os


def url_nature_book(url):
    book_urls = []
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    book_site_urls = soup.find_all("table", class_="d_book")
    for book_url in book_site_urls:
        book_url = book_url.find("a")["href"]
        book_url = urljoin("https://tululu.org", book_url)
        book_urls.append(book_url)
    return book_urls


def save_json(book_elements):
    book_json = json.dumps(book_elements, ensure_ascii=False).encode("utf8")

    with open("book_elements.json", "w", encoding="utf8") as json_file:
        json.dump(book_elements, json_file, ensure_ascii=False)


def main():
    books_elements = []
    for index in range(1, 2):
        natune_book_url = f"https://tululu.org/l55/{index}"
        book_urls = url_nature_book(natune_book_url)

        for book_url in book_urls:
            url_safe_book = "https://tululu.org/txt.php"
            number_book = urlparse(book_url).path
            params = {"id": number_book[2:-1]}
            try:
                response = requests.get(url_safe_book, params=params)
                response.raise_for_status()
                check_for_redirect(response)

                page_response = requests.get(book_url)
                page_response.raise_for_status()
                check_for_redirect(page_response)

                book_elements = parse_book_page(page_response)
                name_img = os.path.split(book_elements["cover_path"])[-1]
                books_elements.append(
                    {
                        "author": book_elements["author"],
                        "title": book_elements["title"],
                        "img_src": f"images/{name_img}",
                        "book_path": f"books/{book_elements['title']}.txt",
                        "comments": book_elements["comments"],
                        "genres": book_elements["genres"],
                    }
                )

                # download_txt(response, book_elements["title"])
                # download_image(book_elements["cover_path"], book_url)

            except requests.HTTPError:
                print("Книга не найдена")
            except requests.ConnectionError:
                print("Произошла ошибка подключения.")
                time.sleep(10)

    save_json(books_elements)


if "__main__" == __name__:
    main()
