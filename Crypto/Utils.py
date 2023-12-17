import sys
if sys.platform == 'darwin':
    sys.path.append('/private/var/tmp/sage-10.2-current/local/var/lib/sage/venv-python3.11.1/lib/python3.11/site-packages')

from functools import reduce
from sage.all import var, GF, PolynomialRing, Integer, Zmod, IntegerRing
from sage.matrix.berlekamp_massey import berlekamp_massey
from string import ascii_lowercase
from itertools import cycle
from math import log10, gcd
from gmpy2 import iroot, isqrt
from Crypto.PublicKey import RSA
from tqdm import trange
import requests


def xor(*args):
    """
    - input : `a (bytes)`, `b (bytes)`, ...
    - output : `result (bytes)` , input bytes' xor, the output length will be the shortest input's length
    """

    return bytes([reduce(lambda i, j : i ^ j, l) for l in zip(*args)])


def egcd(a: int, b: int):
    """
    - input : a(int), b(int) , (a != 0 and b != 0)
    - output : (x, y) (int, int) that satisfy ax + by = gcd(a, b)
    """

    assert (a != 0) and (b != 0)

    a, coe_a =  (a, (1, 0)) if (a > 0) else (-a, (-1, 0))
    b, coe_b =  (b, (0, 1)) if (b > 0) else (-b, (0, -1))
    q, r = a // b, a % b
    while r:
        a, b, coe_a, coe_b = b, r, coe_b, (coe_a[0] - q * coe_b[0], coe_a[1] - q * coe_b[1])
        q, r = a // b, a % b

    return coe_b


def crt(ai_list: list[int], mi_list: list[int]):
    """
    - input : `ai_list (list[int])`, `mi_list (list[int])` , and assume `ai_list = [a1, a2, ...]`, `mi_list = [m1 ,m2, ...]`
        - `x ≡ a1 (mod m1)`
        - `x ≡ a2 (mod m2)`
        - ...
    - output : `x % M (int)` , `M = m1 * m2 * ...`
    """
    assert len(ai_list) == len(mi_list)

    M = reduce(lambda x, y: x * y, mi_list)
    Mi_list = [M // mi for mi in mi_list]
    ti_list = [pow(Mi, -1, mi) for Mi, mi in zip(Mi_list, mi_list)]
    return sum(ai * ti * Mi for ai, ti, Mi in zip(ai_list, ti_list, Mi_list)) % M


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


def polynomialgcd(f1, f2):
    """
    - input : `f1 (polynomial)`, `f2 (polynomial)`
    - output : `f_gcd (polynomial)` , `gcd(f1, f2)`
    """
    if f2 == 0:
        return f1.monic()
    if f2.degree() > f1.degree():
        f1, f2 = f2, f1

    while f2 != 0:
        f1, f2 = f2, f1 % f2
    return f1.monic()


def un_bitshift_right_xor(value: int, shift: int):
    """
    - input : `value (int)`, `shift (int)`
    - output : `result (int)` , `value = (result >> shift) ^ result`
    """

    i = 0
    result = 0
    while ((i * shift) < 32):
        partmask = int('1' * shift + '0' * (32 - shift), base = 2) >> (shift * i)
        part = value & partmask
        value ^= (part >> shift)
        result |= part
        i += 1
    return result


def un_bitshift_left_xor_mask(value: int, shift: int, mask: int):
    """
    - input : `value (int)`, `shift (int)`, `mask (int)`
    - output : `result (int)` , `value = ((result << shift) & mask) ^ result`
    """

    i = 0
    result = 0
    while ((i * shift) < 32):
        partmask = int('0' * (32 - shift) + '1' * shift, base = 2) << (shift * i)
        part = value & partmask
        value ^= (part << shift) & mask
        result |= part
        i += 1
    return result

