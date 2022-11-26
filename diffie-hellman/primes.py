import random
from typing import Iterator


def bits(n: int) -> Iterator[int]:
    while n:
        lsb = n % 2
        yield lsb
        n //= 2


def fast_power(a: int, b: int, m: int):
    s, c = 1, a
    for bit in bits(b):
        if bit:
            s = s * c % m
        c = c**2 % m
    return s


def jacobi(a: int, b: int) -> int:
    a = a % b
    sign = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            rem = b % 8
            if rem in (3, 5):
                sign = -sign
        a, b = b, a
        if a % 4 == 3 and b % 4 == 3:
            sign = -sign
        a = a % b
    if b == 1:
        return sign
    return 0


def solovay_strassen_test(n: int, rounds: int | None = None) -> bool:
    """
    returns true if number is probably prime, returns false otherwise
    """
    rounds = rounds or n.bit_length() + 1

    for _ in range(rounds):
        a = random.randint(2, n-1)
        x = jacobi(a, n)
        if x == 0 or fast_power(a, (n-1)//2, n) != x % n:
            return False

    return True


def get_random(bitlen: int) -> int:
    return random.randint(2**(bitlen-1)+1, 2**bitlen)


def get_random_prime(bitlen: int) -> int:
    while True:
        n = get_random(bitlen)
        if solovay_strassen_test(n):
            return n


if __name__ == "__main__":
    assert jacobi(1001, 9907) == -1
    assert jacobi(19, 45) == 1
    assert jacobi(8, 21) == -1

    assert not solovay_strassen_test(2**20)
    assert solovay_strassen_test(19)
    assert solovay_strassen_test(289189302323613847636698594589)
    assert not solovay_strassen_test(3 * 5 * 7 * 11 * 13 * 17)

    print(get_random_prime(200))
