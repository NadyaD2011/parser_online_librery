from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape


def read_json():
    with open("book_elements.json", "r", encoding="utf-8") as my_file:
        json_file = my_file.read()

    book_elements = json.loads(json_file)
    return book_elements


def main():
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")
    book_elements = read_json()
    rendered_page = template.render(
        book_elements=book_elements,
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(
        ("0.0.0.0", 8000),
        SimpleHTTPRequestHandler,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
