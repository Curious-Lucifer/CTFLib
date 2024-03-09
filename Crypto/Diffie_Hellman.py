from .Utils import *


def ElGamal_nohash_fakesig(g: int, y: int, p: int):
    """
    - input : `g (int)`, `y (int)`, `p (int)`
    - output : `r, s, m (int, int, int)`
    """

    nbits = p.bit_length()
    e, v = getPrime(nbits - 1), getPrime(nbits - 1)

    r = (pow(g, e, p) * pow(y, v, p)) % p
    s = (-r * pow(v, -1, p - 1)) % (p - 1)
    m = (e * s) % (p - 1)

    return r, s, m


def DSA_reuse_nonce(msg1_h: int, msg2_h: int, r1: int, s1: int, r2: int, s2: int, q: int):
    """
    - input : `msg1_h (int)`, `msg2_h (int)`, `r1 (int)`, `s1 (int)`, `r2 (int)`, `s2 (int)`, `q (int)`
    - output : `k (int)`, `x (int)`
    """

    k = ((msg2_h - msg1_h) * pow(s2 - s1, -1, q)) % q
    x = (pow(r1, -1, q) * (s1 * k - msg1_h)) % q
    return k, x

