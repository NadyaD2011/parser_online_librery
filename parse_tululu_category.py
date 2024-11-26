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
    book_site_urls = soup.select("table.d_book")
    for book_url in book_site_urls:
        book_url = book_url.select_one("a")["href"]
        book_url = urljoin("https://tululu.org", book_url)
        book_urls.append(book_url)
    return book_urls


def save_json(books_elements):
    with open("book_elements.json", "w", encoding="utf8") as json_file:
        json.dump(books_elements, json_file, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Программа скачивает книги с сайта tululu.org и достаёт данные о книге"
    )
    parser.add_argument(
        "-start", "--start_page", help="Первая книганужная вам", default=1, type=int
    )
    parser.add_argument(
        "-end", "--end_page", help="Последняя книга нужная вам", default=701, type=int
    )
    parser.add_argument(
        "-folder",
        "--dest_folder",
        help="Путь к каталогу с результатами парсинга",
        default="media",
        type=str,
        action="store",
    )
    parser.add_argument(
        "-skip_imgs",
        "--skip_imgs",
        help="Не скачивать картинки",
        default=False,
        action="store_false",
    )
    parser.add_argument(
        "-skip_txt",
        "--skip_txt",
        help="Не скачивать текс",
        default=False,
        action="store_false",
    )
    args = parser.parse_args()

    books_elements = []
    for index in range(args.start_page, args.end_page):
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
                        "img_src": f"{args.dest_folder}/images/{name_img}",
                        "book_path": f"{args.dest_folder}/books/{book_elements['title']}.txt",
                        "comments": book_elements["comments"],
                        "genres": book_elements["genres"],
                    }
                )

                if not (args.skip_imgs):
                    download_image(book_elements["cover_path"], book_url)
                if not (args.skip_txt):
                    download_txt(response, book_elements["title"])

            except requests.HTTPError:
                print("Книга не найдена")
            except requests.ConnectionError:
                print("Произошла ошибка подключения.")
                time.sleep(10)

    save_json(books_elements)


if "__main__" == __name__:
    main()
