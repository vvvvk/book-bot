from typing import Dict, Tuple
# BOOK_PATH = 'books/book.txt'
BOOK_PATH = 'books/Bredberi_Marsianskie-hroniki.txt'

PAGE_SIZE = 1050

book: Dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> Tuple[str, int]:
    if start+size >= len(text):
        return text[start:], len(text[start:])
    end = start+size
    while text[end-1] not in ',.!:;?' or (end < len(text) and text[end] == '.'):
        end -= 1

    return text[start:end], end-start


def prepare_book(path: str) -> None:
    global book
    with open(path) as file:
        text = file.read().strip()
    start, page = 0, 1
    while start < len(text):
        tmp, size = _get_part_text(text, start, PAGE_SIZE)
        book[page] = tmp.lstrip()
        start += size
        page += 1


prepare_book(BOOK_PATH)
