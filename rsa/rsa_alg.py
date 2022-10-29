from dataclasses import dataclass
from typing import Iterator, List
from primes import get_random_prime, get_random
from euclid import egcd
import math


@dataclass(frozen=True)
class PublicKey:
    n: int
    e: int


@dataclass(frozen=True)
class PrivateKey:
    n: int
    d: int


@dataclass(frozen=True)
class Keypair:
    public: PublicKey
    private: PrivateKey


@dataclass
class KeypairGenerationResult:
    keypair: Keypair
    p: int
    q: int
    totient: int


def generate_keypair(primes_size: int) -> KeypairGenerationResult:
    """
    returns p, q, totient function
    """
    p, q = get_random_prime(primes_size), get_random_prime(primes_size)
    totient = (p-1) * (q-1)
    n = p * q
    while True:
        e = get_random(math.ceil(n.bit_length() / 3))
        gcd, x, _ = egcd(e, totient)
        if gcd == 1:
            d = x % totient
            break
    privKey = PrivateKey(n, d)
    pubKey = PublicKey(n, e)
    keypair = Keypair(pubKey, privKey)
    return KeypairGenerationResult(keypair, p, q, totient)


def bits(n: int) -> Iterator[int]:
    while n:
        lsb = n % 2
        yield lsb
        n //= 2


def pow(a: int, b: int, m: int):
    s, c = 1, a
    for bit in bits(b):
        if bit:
            s = s * c % m
        c = c**2 % m
    return s


def encrypt(data: int, key: PublicKey) -> int:
    assert data < key.n
    return pow(data, key.e, key.n)


def decrypt(enc_data: int, key: PrivateKey) -> int:
    assert enc_data < key.n
    return pow(enc_data, key.d, key.n)


if __name__ == "__main__":
    res = generate_keypair(10)
    print(res)
    keypair = res.keypair
    data = ord("A")
    msg = encrypt(data, keypair.public)
    print(f"msg = {msg}")
    decrypted = chr(decrypt(msg, keypair.private))
    print(f"decrypted = {decrypted}")
