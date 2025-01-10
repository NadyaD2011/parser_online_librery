import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def read_json():
    with open("book_elements.json", "r", encoding="utf-8") as my_file:
        json_file = my_file.read()

    book_elements = json.loads(json_file)
    return book_elements


def on_reload():
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")
    book_elements = read_json()
    paired_books = chunked(book_elements, 2)
    rendered_page = template.render(
        paired_books=paired_books,
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == "__main__":
    main()
