import random


class MT19937_Manager:
    def __init__(self):
        self._state = []
        self._idx = 0

    def setrandbits(self, bits: int, rand: int):
        if (bits % 32) != 0:
            raise ValueError('`bits` must be multiple of 32')
        if hasattr(self, '_random_Random'):
            raise ValueError('`random.Random` object has already been initialized')

        for i in range(0, bits, 32):
            if len(self._state) < 624:
                self._state.append(
                    MT19937_Manager.rand2state((rand >> i) & 0xffffffff)
                )

            elif (self._idx % 624) == 0:
                self.flush_state()
                self._idx = 0

            self._idx += 1

    def getrandbits(self, bits: int):
        if len(self._state) != 624:
            raise ValueError('length of `state` is not equal to 624')

        if not hasattr(self, '_random_Random'):
            self.get_random_Random()

        return self._random_Random.getrandbits(bits)

    def get_random_Random(self):
        if hasattr(self, '_random_Random'):
            return self._random_Random
        else:
            if len(self._state) != 624:
                raise ValueError('length of `state` is not equal to 624')
            
            random_Random = random.Random()
            random_Random.setstate((3, tuple(self._state + [self._idx]), None))
            self._random_Random = random_Random
            return random_Random

    @staticmethod
    def un_bitshiftright_xor(value: int, shift: int):
        i = 0
        result = 0
        while ((i * shift) < 32):
            partialmask = int('1' * shift + '0' * (32 - shift), base = 2) >> (shift * i)
            partial = value & partialmask
            value ^= (partial >> shift)
            result |= partial
            i += 1
        return result

    @staticmethod
    def un_bitshiftleft_xor_mask(value: int, shift: int, mask: int):
        i = 0
        result = 0
        while ((i * shift) < 32):
            partialmask = int('0' * (32 - shift) + '1' * shift, base = 2) << (shift * i)
            partial = value & partialmask
            value ^= (partial << shift) & mask
            result |= partial
            i += 1
        return result

    @staticmethod
    def random2state(value: int):
        if value.bit_length() > 32:
            raise ValueError('`value`\'s bit larger is greater than 32')

        value = MT19937_Manager.un_bitshiftright_xor(value, 18)
        value = MT19937_Manager.un_bitshiftleft_xor_mask(value, 15, 0xefc60000)
        value = MT19937_Manager.un_bitshiftleft_xor_mask(value, 7, 0x9d2c5680)
        value = MT19937_Manager.un_bitshiftright_xor(value, 11)
        return value

    @staticmethod
    def state2random(value: int):
        if value.bit_length() > 32:
            raise ValueError('`value`\'s bit larger is greater than 32')

        value ^= value >> 11
        value ^= (value << 7) & 0x9d2c5680
        value ^= (value << 15) & 0xefc60000
        value ^= value >> 18
        return value

    @staticmethod
    def flush_state(state: list[int]):
        if len(state) != 624:
            raise ValueError('`state`\'s length is not equal to 624')
        
        new_state = state.copy()
        for i in range(624):
            y = (new_state[i] & 0x80000000) + (new_state[(i + 1) % 624] & 0x7fffffff)
            next = y >> 1
            next ^= new_state[(i + 397) % 624]
            if ((y & 1) == 1):
                next ^= 0x9908b0df
            new_state[i] = next
        return new_state


class PythonRandom_64BitsSeed_Manager:
    def __init__(self, continue_rands0: list[int], continue_rands1: list[int], start_idx: int):
        # if start_idx = 227
        #     index of `continue_rands0` will be 227 228 229 230
        #     index of `continue_rands1` will be   0   1   2   3 (+397)
        if not (227 <= start_idx <= 619):
            raise ValueError('`start_idx` shoud satisfy 227 ≤ `start_idx` ≤ 619')
        if len(continue_rands0) != 4:
            raise ValueError('`continue_rands0`\'s length shoud be equal to 4')
        if len(continue_rands1) != 4:
            raise ValueError('`continue_rands1`\'s length shoud be equal to 4')

        self._continue_rands0 = continue_rands0.copy()
        self._continue_rands1 = continue_rands1.copy()
        self._start_idx = start_idx

    def _continue_rands2states(self):
        self._continue_states0 = [MT19937_Manager.random2state(rand) for rand in self._continue_rands0]
        self._continue_states1 = [MT19937_Manager.random2state(rand) for rand in self._continue_rands1]

    def _get_init_continue_states0(self):
        self._init_continue_states0 = [0]
        for state0, state1 in zip(self._continue_states0, self._continue_states1):
            state = state0 ^ state1
            if (state >> 31):
                state ^= 0x9908b0df
                state = (state << 1) | 1
            else:
                state <<= 1
            self._init_continue_states0[-1] |= (state & 0x80000000)
            self._init_continue_states0.append(state & 0x7fffffff)

    def _get_seed(self):
        states = []
        for i in range(1, 4):
            prestate = self._init_continue_states0[i]
            prestate = ((prestate ^ (prestate >> 30)) * 1566083941) & 0xffffffff
            state = (self._init_continue_states0[i + 1] + self._start_idx + i + 1) & 0xffffffff
            states.append(state ^ prestate)

        initial_states = self.generate_initial_states()
        key = [0, 0]
        for i in range(1, 3):
            prestate = ((states[i - 1] ^ (states[i - 1] >> 30)) * 1664525) & 0xffffffff
            key[(self._start_idx + i + 1) % 2] = (states[i] - (initial_states[self._start_idx + i + 2] ^ prestate)- ((self._start_idx + i + 1) % 2)) & 0xffffffff
        
        seed = key[0] | (key[1] << 32)
        if PythonRandom_64BitsSeed_Manager.seed2initial_states(seed)[self._start_idx + 4] == self._init_continue_states0[4]:
            self._seed = seed
        else:
            self._init_continue_states0[4] |= 0x80000000
            self._get_seed()

    def get_seed(self):
        if not hasattr(self, '_seed'):
            self._continue_rands2states()
            self._get_init_continue_states0()
            self._get_seed()
        return self._seed

    @staticmethod
    def generate_initial_states():
        state = [19650218]
        for i in range(1, 624):
            state.append((1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xffffffff)
        return state

    @staticmethod
    def seed2initial_states(seed: int):
        bits = seed.bit_length()
        if (bits <= 32) or (bits > 64):
            raise ValueError('`seed`\'s bit length should larger than 32 and less or equal to 64')

        key = [seed & 0xffffffff, (seed >> 32) & 0xffffffff]
        states = PythonRandom_64BitsSeed_Manager.generate_initial_states()

        i, j = 1, 0
        for _ in range(624):
            prestate = ((states[i - 1] ^ (states[i - 1] >> 30)) * 1664525) & 0xffffffff
            states[i] = ((states[i] ^ prestate) + key[j] + j) & 0xffffffff
            i += 1
            if (i >= 624): 
                states[0] = states[-1]
                i = 1
            j = (j + 1) % 2

        for _ in range(623):
            prestate = ((states[i - 1] ^ (states[i - 1] >> 30)) * 1566083941) & 0xffffffff
            states[i] = ((states[i] ^ prestate) - i) & 0xffffffff
            i += 1
            if (i >= 624):
                states[0] = states[-1]
                i = 1

        states[0] = 0x80000000

        return states

