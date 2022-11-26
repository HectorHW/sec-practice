from math import ceil, sqrt


def baby_giant(y: int, g: int, p: int):
    """
    computes x: y = g^x mod p
    """
    m = ceil(sqrt(p))
    table = {}
    e1 = pow(g, m, p)
    exp = e1
    for i in range(1, m+1):
        table[exp] = i
        exp = exp * e1 % p

    gamma = y
    for j in range(m):
        if gamma in table:
            return table[gamma] * m - j
        gamma = gamma * g % p


if __name__ == "__main__":
    print(baby_giant(3, 5, 23))
    assert baby_giant(3, 5, 23) == 16
