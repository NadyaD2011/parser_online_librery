import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def read_json():
    with open("book_elements.json", "r", encoding="utf-8") as my_file:
        json_file = my_file.read()

    book_elements = json.loads(json_file)
    return book_elements


def main():
    page_folder = "pages"
    os.makedirs(page_folder, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("/template/template.html")
    book_elements = read_json()
    books_pages = list(chunked(book_elements, 10))
    total_pages = len(books_pages)

    for number, books_page in enumerate(books_pages):
        rendered_page = template.render(
            paired_books=chunked(books_page, 2),
            page_number=number + 1,
            total_pages=total_pages,
        )
        page_path = f"{page_folder}/index{number + 1}.html"
        with open(page_path, "w", encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    main()
