from enum import Enum
import string


class EncodingAlphabet(str, Enum):
    RUSSIAN = "RU"
    ENGLISH = "EN"

    def get_alphabet_string(self) -> str:
        RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        NUMBERS = "0123456789"
        if self.value == "RU":
            return RUSSIAN_LETTERS + NUMBERS
        return string.ascii_lowercase + NUMBERS

    def __str__(self) -> str:
        return self


def encode_ceasar(alphabet: EncodingAlphabet, message: str, offset: int) -> str:
    alphabet = alphabet.get_alphabet_string()
    if any(letter not in alphabet and not letter.isspace() for letter in message):
        raise ValueError

    offset = offset % len(alphabet)

    def encode_letter(letter: str) -> str:
        if letter not in alphabet:
            return letter
        position = alphabet.index(letter)
        encoded = (position + offset) % len(alphabet)
        return alphabet[encoded]

    return "".join(map(encode_letter, message))


def decode_ceasar(alphabet: EncodingAlphabet, message: str, offset: int) -> str:
    return encode_ceasar(alphabet, message, -offset)
