import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server
import argparse


def on_reload():
    parser = argparse.ArgumentParser(
        description="Программа хочет получить путь до файла(json) с данными о книгах"
    )
    parser.add_argument(
        "--json_file",
        help="Путь к каталогу с результатами парсинга",
        default="static/book_elements.json",
        action="store",
        type=str
    )
    args = parser.parse_args()

    page_folder = "pages"
    number_books = 10
    number_col = 2
    os.makedirs(page_folder, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("/template/template.html")

    with open(args.json_file, "r", encoding="utf-8") as my_file:
        book_elements = json.load(my_file)
    
    books_pages = list(chunked(book_elements, number_books))
    total_pages = len(books_pages)

    for number, books_page in enumerate(books_pages, 1):
        rendered_page = template.render(
            paired_books=chunked(books_page, number_col),
            page_number=number,
            total_pages=total_pages,
        )
        page_path = f"{page_folder}/index{number}.html"
        with open(page_path, "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch("template/template.html", on_reload)
    server.serve(root=".", default_filename="pages/index1.html")


if __name__ == "__main__":
    main()
