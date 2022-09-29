from itertools import cycle
from enum import Enum
import string
RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
NUMBERS = "0123456789"


class EncodingAlphabet(str, Enum):
    RUSSIAN = "RU"
    ENGLISH = "EN"

    def get_alphabet_string(self) -> str:
        RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        NUMBERS = "0123456789"
        if self.value == "RU":
            return RUSSIAN_LETTERS + NUMBERS
        return string.ascii_lowercase + NUMBERS

    def get_key_string(self) -> str:
        if self.value == "RU":
            return RUSSIAN_LETTERS
        return string.ascii_lowercase

    def __str__(self) -> str:
        return self


class UnsupportedMessage(ValueError):
    pass


class UnsupportedKey(ValueError):
    pass


def _bailout_on_unexpected_chars(alphabet: str, message: str):
    def predicate(symbol: str) -> bool:
        return symbol not in alphabet and not symbol.isspace()
    if errors := list(filter(predicate, message)):
        raise UnsupportedMessage(errors)


def _bailout_on_unexpected_key(key_alphabet: str, key: str):
    if errors := list(filter(lambda item: item not in key_alphabet, key)):
        raise UnsupportedKey(errors)


def transform_vigenere(alphabet: EncodingAlphabet, message: str, key: str, inv=False) -> str:
    if not key:
        return message
    alphabet, key_alphabet = alphabet.get_alphabet_string(), \
        alphabet.get_key_string()
    _bailout_on_unexpected_chars(alphabet, message)
    _bailout_on_unexpected_key(key_alphabet, key)

    def encode_letter(letter: str, offset_letter: str) -> str:
        if letter not in alphabet:
            return letter
        position = alphabet.index(letter)
        shift = key_alphabet.index(offset_letter) * (-1 if inv else 1)
        encoded = (position + shift) % len(alphabet)
        return alphabet[encoded]

    return "".join(map(encode_letter, message, cycle(key)))
