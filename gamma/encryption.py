import random
from itertools import cycle
RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
NUMBERS = "0123456789"


def encrypt(text: str, key: str) -> str:
    return "".join(
        map(lambda t, k: ('1' if t != k else '0'), text, cycle(key))
    )


def generate_key(size: int) -> str:
    symbols = list('0' * (size // 2) + '1' * (size // 2) +
                   ("" if size % 2 == 0 else random.choice('01')))
    random.shuffle(symbols)
    return "".join(symbols)
