from sage.all import GF
from sage.matrix.berlekamp_massey import berlekamp_massey
from functools import reduce
from math import gcd
from .Utils import un_bitshift_left_xor_mask, un_bitshift_right_xor


def lcg_next(s: int, m: int, inc: int, N: int):
    """
    - input : `s (int)`, `m (int)`, `inc (int)`, `N (int)`
    - output : `s_next (int)` , `s_next = (m * s + inc) % N`
    """
    
    return (m * s + inc) % N


def lcg_attack(state: list[int]):
    """
    - input : `state (list[int])` , that `state[i] = (state[i - 1] * m + inc) % N`
    - output : `(m, inc, N) (int, int, int)`
    """

    diff_list = [s1 - s0 for s0, s1 in zip(state, state[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diff_list, diff_list[1:], diff_list[2:])]
    N = abs(reduce(gcd, zeroes))

    m = (diff_list[1] * pow(diff_list[0], -1, N)) % N
    inc = (state[1] - state[0] * m) % N

    return int(m), int(inc), N


def lfsr_attack(lfsr_list: list[int], register_length: int, length: int):
    """
    - input : `lfsr_list (list[int])`, `register_length (int)`, `length (int)` , `len(lfsr_list) > register_length`
    - output : `lfsr_list (list[int])` , `len(lfsr_list) == length`
    """

    G = GF(2)
    lfsr_list = [G(num) for num in lfsr_list]
    coefficient_list = berlekamp_massey(lfsr_list).list()[:-1]
    coefficient_list_length = len(coefficient_list)

    lfsr_list = lfsr_list[:register_length]
    for _ in range(length - register_length):
        lfsr_list.append(sum([lfsr_list[-coefficient_list_length + i] * coefficient_list[i] for i in range(coefficient_list_length)]))
    return [int(num) for num in lfsr_list]


def MT19937_rand2state(value: int):
    """
    - input : `value (int)`
    - output : `value (int)` , for MT19937
    """

    value = un_bitshift_right_xor(value, 18)
    value = un_bitshift_left_xor_mask(value, 15, 0xefc60000)
    value = un_bitshift_left_xor_mask(value, 7, 0x9d2c5680)
    value = un_bitshift_right_xor(value, 11)
    return value


def MT19937_state2rand(value: int):
    """
    - input : `value (int)`
    - output : `value (int)` , for MT19937
    """

    value ^= (value >> 11)
    value ^= (value << 7) & 0x9d2c5680
    value ^= (value << 15) & 0xefc60000
    value ^= (value >> 18)
    return value


def MT19937_gen_next_state(state: list[int]):
        """
        - input : `state (list[int])` , `state` will be changed to next state
        - output : None
        """

        assert len(state) == 624
        for i in range(624):
            y = (state[i] & 0x80000000) + (state[(i + 1) % 624] & 0x7fffffff)
            next = y >> 1
            next ^= state[(i + 397) % 624]
            if ((y & 1) == 1):
                next ^= 0x9908b0df
            state[i] = next


def MT19937_attack(rand_list: list[int], n: int):
    """
    - input : `rand_list (list[int])`, `n (int)` , `rand_list` is the first 624's 32 bits random number's list
    - output : `random_num (int)` , the `n`'s random number, if `n == 0`, `random_num = rand_list[0]`
    """

    if n < 624:
        return rand_list[n]

    state = [MT19937_rand2state(r) for r in rand_list]
    for _ in range(n // 624):
        MT19937_gen_next_state(state)
    return MT19937_state2rand(state[n % 624])

