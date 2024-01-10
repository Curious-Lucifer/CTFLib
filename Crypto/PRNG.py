from .Utils import *


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


class MT19937_z3_Attack:
    def __init__(self):
        self.state_idx = 0
        self.state = [z3.BitVec(f'state_{self.state_idx}[{i}]', 32) for i in range(624)]
        self.idx = 0
        self.solver = z3.Solver()
        self.counter = count()
        self.checknum = 0
        self.real_state = None

    def rand2state(self, r_symbol):
        label = next(self.counter)

        s_symbol = z3.BitVec(f's_symbol_{label}', 32)
        num0 = z3.BitVec(f'num0_{label}', 32)
        num1 = z3.BitVec(f'num1_{label}', 32)
        num2 = z3.BitVec(f'num2_{label}', 32)

        self.solver.add([
            num0 == s_symbol ^ (z3.LShR(s_symbol, 11)), 
            num1 == num0 ^ ((num0 << 7) & 0x9D2C5680),
            num2 == num1 ^ ((num1 << 15) & 0xEFC60000),
            r_symbol == num2 ^ (z3.LShR(num2, 18))
        ])

        return s_symbol

    def gen_next_state(self):
        state = self.state.copy()

        for i in range(624):
            y = (state[i] & 0x80000000) + (state[(i + 1) % 624] & 0x7fffffff)
            n = z3.LShR(y, 1)
            n = n ^ state[(i + 397) % 624]
            n = z3.If(y & 1 == 1, n ^ 0x9908b0df, n)
            state[i] = n

        return state

    def setrandbits(self, randbits: str):
        assert len(randbits) == 32
        assert all(map(lambda x: x in '01?', randbits))

        if self.idx == 624:
            next_state = self.gen_next_state()
            self.state_idx += 1
            self.state = [z3.BitVec(f'state_{self.state_idx}[{i}]', 32) for i in range(624)]
            for i in range(624):
                self.solver.add(self.state[i] == next_state[i])
            self.idx = 0

        label = next(self.counter)

        r_symbol = z3.BitVec(f'r_symbol_{label}', 32)
        for i, bit in enumerate(reversed(randbits)):
            if bit != '?':
                self.checknum += 1
                self.solver.add(z3.Extract(i, i, r_symbol) == bit)
        s_symbol = self.rand2state(r_symbol)

        self.solver.add(self.state[self.idx] == s_symbol)
        self.idx += 1

    def getRandomObj(self):
        assert self.checknum >= 624 * 32

        if self.real_state is None:
            print('[\033[1m\033[92m+\033[0m\033[0m] Calculating Current State')
            st_time = time()

            assert self.solver.check() == z3.sat

            model = self.solver.model()
            print(f'[\033[94m*\033[0m] {int(time() - st_time)}s Calculation completed')

            self.real_state = list(map(lambda x: model[x].as_long(), self.state))

        r = random.Random()
        r.setstate((3, tuple(self.real_state + [self.idx]), None))

        return r

