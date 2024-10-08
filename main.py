import requests
import os


def save_file(book_id, directory):
    url = f"https://tululu.org/txt.php?id={book_id}"
    response = requests.get(url)
    response.raise_for_status()

    filename = f"id_{book_id+1}.txt"
    with open(f"{directory}/{filename}", "wb") as file:
        file.write(response.content)


def create_path(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    directory = "books"
    create_path(directory)
    for book_id in range(10):
        save_file(book_id, directory)


if "__main__" == __name__:
    main()
