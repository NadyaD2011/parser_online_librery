import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server


def read_json(name_json_file="book_elements.json"):
    with open(name_json_file, "r", encoding="utf-8") as my_file:
        json_file = my_file.read()

    book_elements = json.load(json_file)
    return book_elements


def on_reload():
    page_folder = "pages"
    name_json_file = "book_elements.json"
    number_books = 10
    os.makedirs(page_folder, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("/template/template.html")
    book_elements = read_json(name_json_file)
    books_pages = list(chunked(book_elements, number_books))
    total_pages = len(books_pages)

    for number, books_page in enumerate(books_pages, 1):
        rendered_page = template.render(
            paired_books=chunked(books_page, 2),
            page_number=number,
            total_pages=total_pages,
        )
        page_path = f"{page_folder}/index{number}.html"
        with open(page_path, "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch("/template/template.html", on_reload)
    server.serve(root=".", default_filename="pages/index1.html")


if __name__ == "__main__":
    main()
