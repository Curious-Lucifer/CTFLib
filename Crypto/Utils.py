from functools import reduce


def xor(*args):
    """
    - input : `a (bytes)`, `b (bytes)`, ...
    - output : `result (bytes)` , input bytes' xor, the output length will be the shortest input's length
    """

    return bytes([reduce(lambda i, j : i ^ j, l) for l in zip(*args)])


def egcd(a: int, b: int):
    """
    input : a(int), b(int) , (a != 0 and b != 0)
    output : (x, y) (int, int) that satisfy ax + by = gcd(a, b)
    """

    assert (a != 0) and (b != 0)

    a, coe_a =  (a, (1, 0)) if (a > 0) else (-a, (-1, 0))
    b, coe_b =  (b, (0, 1)) if (b > 0) else (-b, (0, -1))
    q, r = a // b, a % b
    while r:
        a, b, coe_a, coe_b = b, r, coe_b, (coe_a[0] - q * coe_b[0], coe_a[1] - q * coe_b[1])
        q, r = a // b, a % b
    
    return coe_b


def crt(a_list: list[int], m_list: list[int]):
    """
    - input : `a_list (list[int])`, `m_list (list[int])` , and assume `a_list = [a1, a2, ...]`, `m_list = [m1 ,m2, ...]`
        - `x ≡ a1 (mod m1)`
        - `x ≡ a2 (mod m2)`
        - ...
    - output : `x % M (int)` , `M = m1 * m2 * ...`
    """
    assert len(a_list) == len(m_list)

    M = reduce(lambda x, y: x * y, m_list)
    Mi_list = [M // m for m in m_list]
    ti_list = [pow(Mi, -1, m) for Mi, m in zip(Mi_list, m_list)]
    return sum(a * ti * Mi for a, ti, Mi in zip(a_list, ti_list, Mi_list)) % M


def lcg_generate(seed: int, m: int, inc: int, N: int, num: int):
    """
    - input : `seed (int)`, `m (int)`, `inc (int)`, `N (int)`, `num (int)`
    - output : `s (int)` , `seed = state[0]` , `s = state[num]`
    """

    s = seed
    for _ in range(num):
        s = (m * s + inc) % N

    return s


def legendre_symbol(a: int, p: int):
    """
    - input : `a (int)`, `p (int)`
    - output : `ls (int)` , value of (a/p) (legendre symbol)
    """

    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == (p - 1) else ls


def ceil_int(a: int, b: int):
    """
    - input : `a (int)`, `b (int)`
    - output : `ceil(a / b) (int)`
    """

    return (a // b) + (a % b > 0)

def floor_int(a: int, b: int):
    """
    - input : `a (int)`, `b (int)`
    - output : `floor(a / b) (int)`
    """

    return a // b

