from itertools import chain
from typing import Dict, Iterable, List, TypeVar
from encryption import EncodingAlphabet
from collections import Counter, defaultdict
import os
from textwrap import wrap
import math


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


def crack_single_shift(text: str, alphabet: EncodingAlphabet) -> Dict[int, float]:

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


def shift_freq_dict(freqs: Dict[str, float], letter_span: str, offset: int) -> Dict[str, float]:
    return {
        letter_span[(letter_span.index(k)+offset) % len(letter_span)]: freqs[k] for k in freqs
    }


def prob_distance(a: Dict[str, float], b: Dict[str, float]) -> float:
    result = 1e-6
    for k in set(chain(a.keys(), b.keys())):
        result += abs(a.get(k, 0) - b.get(k, 0))
    return 1 / result


def crack_shift_brute(text: str, alphabet: EncodingAlphabet) -> Dict[int, float]:
    text_freqs = text_to_freqs(filter_text(text, alphabet), alphabet)
    reference_freqs = alphabet.get_freq_dict()

    result = {}

    for offset in range(len(alphabet.get_alphabet_string())):
        shifted = shift_freq_dict(
            text_freqs, alphabet.get_alphabet_string(), offset)
        proba = prob_distance(shifted, reference_freqs)
        result[(-offset) % len(alphabet.get_alphabet_string())] = proba
    return result


def get_transposed_blocks(text: str, block_size: int) -> List[List[str]]:
    len_limit = len(text) // block_size * block_size
    blocks = wrap(text[:len_limit], block_size)
    return list(zip(*blocks))


T = TypeVar("T")


def recursive_choices(candidates: List[List[T]]) -> Iterable[List[T]]:
    if len(candidates) == 1:
        yield from [[item] for item in candidates[0]]
    else:
        sublist = candidates[1:]
        for item in candidates[0]:
            yield from map(lambda sub: [item]+sub, recursive_choices(sublist))


def top_k_entries(d: Dict[T, float], k=2) -> Dict[T, float]:
    entries = sorted(d.items(), key=lambda item: item[1], reverse=True)[:k]
    return dict(entries)


def crack(text: str, alphabet: EncodingAlphabet, key_size: int) -> Dict[str, float]:
    text = filter_text(text, alphabet)
    cracker = crack_shift_brute
    #cracker = crack_single_shift
    candidate_freqs: List[Dict[int, float]] = [
        cracker("".join(column), alphabet) for column in get_transposed_blocks(text, key_size)
    ]
    results = {}
    top = 3 if key_size < 15 else 2
    for freq_map in recursive_choices(list(map(lambda item: top_k_entries(item, top).items(), candidate_freqs))):
        letters, freqs = map(list, zip(*freq_map))

        codeword = "".join([alphabet.get_alphabet_string()[idx]
                           for idx in letters])
        prob = sum([math.log(f) for f in freqs])
        results[codeword] = prob
    return results


def compute_index(text: str) -> float:
    counts = Counter(text)
    return sum(
        k * (k-1) / (len(text) * (len(text)-1))
        for k in counts.values()
    )


def crack_cypher_length(text: str, alphabet: EncodingAlphabet) -> Dict[int, float]:
    text = filter_text(text, alphabet)
    results = {}
    for block_size in range(1, int(os.environ.get("MAX_KEY_SIZE", default='30'))):
        columns = get_transposed_blocks(text, block_size)
        results[block_size] = sum(map(compute_index, columns)) / len(columns)
    return results


if __name__ == "__main__":
    print(list(recursive_choices([['a', 'b', 'c'], [0, 1]])))
    print(top_k_entries({1: 0.5, 2: 0.3, 3: 0.25, 4: 0.1}, k=2))
