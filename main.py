import requests


def save_file(url):
    response = requests.get(url)
    response.raise_for_status()

    filename = "book.txt"
    with open(filename, "wb") as file:
        file.write(response.content)


def main():
    url = 'https://tululu.org/txt.php?id=32168'
    for i in range(10):
        save_file(url, i)


if "__main__" == __name__:
    main()
