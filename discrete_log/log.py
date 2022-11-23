from math import ceil, sqrt


def baby_giant(y: int, g: int, p: int):
    """
    computes x: y = g^x mod p
    """
    m = ceil(sqrt(p))
    table = {}
    exp = 1
    for j in range(m):
        table[exp] = j
        exp = exp * g % p

    inv = pow(g, -m, p)
    gamma = y
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = gamma * inv % p


if __name__ == "__main__":
    print(baby_giant(3, 5, 23))
    assert baby_giant(3, 5, 23) == 16
