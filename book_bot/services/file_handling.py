BOOK_PATH = 'books/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end = min(len(text), start+size)
    while text[end-1] not in ',.!:;?' or (end < len(text) and text[end] == '.'):
        end -= 1

    return text[start:end], end-start


def prepare_book(path: str) -> None:
    global book
    with open(path) as file:
        text = file.read()
    start, page = 0, 1
    while start < len(text):
        tmp, size = _get_part_text(text, start, PAGE_SIZE)
        book[page] = tmp.lstrip()
        start += size
        page += 1


prepare_book(BOOK_PATH)
