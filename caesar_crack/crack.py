from enum import Enum
from typing import Dict
from encryption import EncodingAlphabet
from collections import Counter, defaultdict
import string


def text_to_freqs(text: str, alphabet: EncodingAlphabet) -> Dict[str, float]:
    counts = Counter(text)
    return {
        k: counts.get(k, 0) / counts.total()
        for k in alphabet.get_alphabet_string()
    }


def greedy_match_freqs(a: Dict[str, float], b: Dict[str, float]) -> Dict[str, str]:
    first_mapping = sorted(a.items(), key=lambda item: item[1], reverse=True)
    second_mapping = sorted(b.items(), key=lambda item: item[1], reverse=True)

    return dict(zip(
        map(lambda item: item[0], second_mapping),
        map(lambda item: item[0], first_mapping),)
    )


def filter_text(text: str, alphabet: EncodingAlphabet) -> str:
    def predicate(symbol: str) -> bool:
        return symbol not in alphabet.get_alphabet_string() and not symbol.isspace()
    if errors := list(filter(predicate, text)):
        raise ValueError(errors)
    return "".join(filter(lambda item: item in alphabet.get_alphabet_string(), text))


def crack(text: str, alphabet: EncodingAlphabet) -> Dict[int, float]:

    text_freqs = text_to_freqs(filter_text(text, alphabet), alphabet)
    reference_freqs = alphabet.get_freq_dict()
    letter_match = greedy_match_freqs(text_freqs, reference_freqs)

    def compute_offset(first, second):
        all_letters = alphabet.get_alphabet_string()
        first, second = all_letters.index(first), all_letters.index(second)
        return (second - first) % len(all_letters)

    offsets = {
        k1: compute_offset(k1, k2) for k1, k2 in letter_match.items()
    }

    candidates = defaultdict(lambda: 0.0)
    for letter, offset in offsets.items():
        candidates[offset] += text_freqs[letter]

    return candidates
