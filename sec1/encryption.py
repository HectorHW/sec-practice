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


def _bailout_on_unexpected_chars(alphabet: str, message: str):
    def predicate(symbol:str)->bool:
        return symbol not in alphabet and not symbol.isspace()
    if errors:=list(filter(predicate, message)):
        raise ValueError(errors)

def encode_caesar(alphabet: EncodingAlphabet, message: str, offset: int) -> str:
    alphabet = alphabet.get_alphabet_string()
    _bailout_on_unexpected_chars(alphabet, message)

    offset = offset % len(alphabet)

    def encode_letter(letter: str) -> str:
        if letter not in alphabet:
            return letter
        position = alphabet.index(letter)
        encoded = (position + offset) % len(alphabet)
        return alphabet[encoded]

    return "".join(map(encode_letter, message))


def decode_caesar(alphabet: EncodingAlphabet, message: str, offset: int) -> str:
    return encode_caesar(alphabet, message, -offset)
