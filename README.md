# Парсер книг с сайта tululu.org: Руководство по использованию и документация

## Оглавление

* [Описание проекта](#описание-проекта)
    * [Как это работает?](#как-это-работает)
    * [Предварительные требования](#предварительные-требования)
    * [Установите зависимости](#установите-зависимости)
* [Скрипты проекта](#cкрипты-проекта)
* [Основные скрипты](#основные-скрипты)
    * [parse_tululu_category.py](#parse_tululu_categorypy)
* [Цель проекта](#цель-проекта)

## Описание проекта

Программа скачивает книги, обложки книг с сайта tululu.org и записывает в json файл данные (автора, название книги, путь до изображения, жанр, коментариии, путь до тексового файла с книгой) о книге.

### Как это работает?

Парсер написан на языке Python с использованием библиотеки [requests](https://pypi.org/project/requests/). И запускается в командной строке и начинает скачивать книги, обложки и данные по книгам.

Парсер достает данные с [сайта](https://tululu.org/l55/) и [сайта](https://tululu.org/)

Особенность - умеет скачивать книги и повсем жанрам, и только фантастику.

### Предварительные требования:

1. Установленный Python версии 3.11 и выше.
2. pip - установщик пакетов Python.
3. Хороший интернет (если нет интернета, будет выводить ошибку)

### Установите зависимости

Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```bash
pip install -r requirements.txt
```

## Скрипты проекта:

* [parse_tululu_category.py](#parse_tululu_categorypy)

## Основные скрипты

### parse_tululu_category.py

#### Что делает скрипт?

С помощью этого инструмента вы можете скачать книги с жанром фантастика.

Для проверки его работы мы запускаем код. И ожидаем ошибки, что у нас нет интернета или ждём когда скачаются книги, обложки и данные о книгах.

#### Как запустить скрипт?

Для запуска напишите в командной строке:

```bash
python parse_tululu_category.py
```

В таком случае программа скачает книги с 1 по 701, скачиваются все книги, обложки и данные в папку *media*.
Если же вам нужны книги в определённом диапазоне, не нужны тексты или обложки, вам нужна создавать папку под другим название то в таком случае напишите в командную строку:

```
python tululu.py -start (число) -end (число) -folder (название папки) -skip_imgs (нужно скачивать картинки(False), не нужно(True)) -skip_txt (нужно скачивать книги(False), не нужно(True))
```

Все аргументы не обязательны, вы можете ввести только нужные вам.


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).