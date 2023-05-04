from functools import reduce
from math import gcd


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


def MT19937_attack(rand_list: list[int], n: int):
    """
    - input : `rand_list (list[int])`, `n (int)` , `rand_list` is the first 624's 32 bits random number's list
    - output : `random_num (int)` , the `n`'s random number, if `n == 0`, `random_num = rand_list[0]`
    """

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

    def rand_to_state(value: int):
        """
        - input : `value (int)`
        - output : `value (int)` , for MT19937
        """

        value = un_bitshift_right_xor(value, 18)
        value = un_bitshift_left_xor_mask(value, 15, 0xefc60000)
        value = un_bitshift_left_xor_mask(value, 7, 0x9d2c5680)
        value = un_bitshift_right_xor(value, 11)
        return value

    def state_to_rand(value: int):
        """
        - input : `value (int)`
        - output : `value (int)` , for MT19937
        """

        value ^= (value >> 11)
        value ^= (value << 7) & 0x9d2c5680
        value ^= (value << 15) & 0xefc60000
        value ^= (value >> 18)
        return value


    def gen_next_state(state: list[int]):
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

    if n < 624:
        return rand_list[n]

    state = [rand_to_state(r) for r in rand_list]
    for _ in range(n // 624):
        gen_next_state(state)

    return state_to_rand(state[n % 624])