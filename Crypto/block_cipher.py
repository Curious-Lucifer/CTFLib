from functools import reduce
from typing import Callable

from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import var, GF, PolynomialRing

from ..Utils import trange, info
from .utils import xor


class PrependOracleManager:
    '''
    ### Example

    ```py

    ```
    '''

    def __init__(self, oracle: Callable[[bytes], bytes]):
        self._oracle = oracle

    def _get_correct_cipher(self):
        info('Prepend Oracle Manager : Getting correct cipher')
        self._correct_ciphers = [self._oracle(b'a' * i) for i in range(16)]

    def _get_secret_length(self):
        if not hasattr(self, '_correct_ciphers'):
            raise ValueError('`_correct_ciphers` undefined')

        min_length = len(self._correct_ciphers[0])
        for i in range(16):
            if len(self._correct_ciphers[i]) > min_length:
                self._secret_length = min_length - i
                break
            if i == 15:
                self._secret_length = min_length - 16

    def _get_secret(self):
        if not hasattr(self, '_correct_ciphers'):
            raise ValueError('`_correct_ciphers` undefined')
        if not hasattr(self, '_secret_length'):
            raise ValueError('`_secret_lengths` undefined')

        secret = b''
        prefix = b'a' * 15
        info('Prepend Oracle Manager : Getting secret')
        for i in trange(self._secret_length, leave=False):
            correct_cipher_block = self._correct_ciphers[(-i - 1) % 16][(i // 16) * 16: (i // 16 + 1) * 16]
            for j in range(256):
                current_cipher_block = self._oracle(prefix + bytes([j]))[:16]
                if current_cipher_block == correct_cipher_block:
                    secret += bytes([j])
                    prefix = prefix[1:] + bytes([j])
                    break
                if j == 255:
                    raise ValueError('something went wrong')
        self._secret = secret

    def attack(self):
        if not hasattr(self, '_correct_ciphers'):
            self._get_correct_cipher()
        if not hasattr(self, '_secret_length'):
            self._get_secret_length()
        if not hasattr(self, '_secret'):
            self._get_secret()
        return self._secret


def padding_oracle_attack(pre_cipher_block: bytes, current_cipher_block: bytes, oracle: Callable[[bytes], bool], length: int = 16):
    '''
    ### Example

    ```py
    def oracle(cipher: bytes):
        r.sendlineafter(b'= ', cipher.hex().encode())
        return b'CORRECT' in r.recvline()

    current_plain_block = padding_oracle_attack(pre_cipher_block, current_cipher_block, oracle)

    # or 

    def oracle(cipher: bytes):
        r.sendlineafter(b'= ', cipher.hex().encode())
        return b'CORRECT' in r.recvline()

    partial_current_plain_block = padding_oracle_attack(pre_cipher_block, current_cipher_block, oracle, 14)
    ```
    '''

    assert 1 <= length <= 16
    assert len(pre_cipher_block) == len(current_cipher_block) == 16

    current_plain_block = b''

    for j in trange(length, leave=False):
        possible_bytes = []

        for i in range(256):
            test_cipher = pre_cipher_block[:15 - j] + bytes([i]) + xor(pre_cipher_block[-j:], current_plain_block, bytes([j + 1] * j)) + current_cipher_block
            if oracle(test_cipher):
                possible_bytes.append(bytes([i]))
                if j == 0:
                    continue
                break

        if len(possible_bytes) == 1:
            possible_byte = possible_bytes[0]
        else:
            possible_byte = possible_bytes[possible_bytes.index(pre_cipher_block[-1:]) ^ 1]
        current_plain_block = xor(possible_byte, bytes([j + 1]), pre_cipher_block[-j - 1: -j if (-j) else None]) + current_plain_block

    return current_plain_block


class GCM_Forbidden_Attack_Manager:
    '''
    ### Example

    ```py
    cipher = ...
    AAD = ...

    def get_data():
        ...
        return AAD, cipher, authtag

    manager = GCM_Forbidden_Attack_Manager()

    while not manager.check():
        manager.append(*get_data())

    authtag = manager.calc_authtag(AAD, cipher)
    H = manager.get_H()
    EJ0 = manager.get_EJ0()
    ```
    '''

    def __init__(
        self, 
        AAD_list: list[bytes] | None = None, 
        cipher_list: list[bytes] | None = None, 
        authtag_list: list[bytes] | None = None
    ):
        self._AAD_list: list[bytes] = AAD_list or []
        self._cipher_list: list[bytes] = cipher_list or []
        self._authtag_list: list[bytes] = authtag_list or []

        x = var('x')
        F = GF(2 ** 128, name='a', modulus = x ** 128 + x ** 7 + x ** 2 + x + 1, names=('a',))
        P = PolynomialRing(F, names=('x',))

        self._a = F._first_ngens(1)[0]
        self._x = P._first_ngens(1)[0]

        self._H = None
        self._EJ0 = None


    def append(self, AAD: bytes, cipher: bytes, authtag: bytes):
        self._AAD_list.append(AAD)
        self._cipher_list.append(cipher)
        self._authtag_list.append(authtag)


    def _bytes2polynomial(self, s: bytes):

        assert len(s) == 16

        bin_s = bin(bytes_to_long(s))[2:].rjust(128, '0')
        return sum(
            int(bit) * self._a ** i for i, bit in enumerate(bin_s)
        )


    def _polynomial2bytes(self, poly):
        bin_l = ['0'] * 128

        for key in poly.polynomial().dict().keys():
            bin_l[key] = '1'

        return long_to_bytes(int(''.join(bin_l), base=2), 16)


    def _merge_ADD_cipher(self, AAD: bytes, cipher: bytes):
        payload = AAD
        if (len(payload) % 16) != 0:
            payload += b'\0' * (16 - len(payload) % 16)

        payload += cipher
        if (len(payload) % 16) != 0:
            payload += b'\0' * (16 - len(payload) % 16)

        return payload + long_to_bytes(len(AAD) * 8, 8) + long_to_bytes(len(cipher) * 8, 8)


    def _calc_possible_H(self, data0: tuple[bytes, bytes, bytes], data1: tuple[bytes, bytes, bytes]):
        AAD0, cipher0, authtag0 = data0
        AAD1, cipher1, authtag1 = data1

        payload0 = self._merge_ADD_cipher(AAD0, cipher0)
        payload1 = self._merge_ADD_cipher(AAD1, cipher1)

        poly0 = sum(
            self._bytes2polynomial(payload0[j: j + 16]) * (self._x ** ((len(payload0) - j) // 16))
            for j in range(0, len(payload0), 16)
        )
        poly1 = sum(
            self._bytes2polynomial(payload1[j: j + 16]) * (self._x ** ((len(payload1) - j) // 16))
            for j in range(0, len(payload1), 16)
        )

        f = poly0 - poly1 + self._bytes2polynomial(authtag1) - self._bytes2polynomial(authtag0)
        return set(self._polynomial2bytes(root) for root, _ in f.roots())


    def _calc_H(self) -> set[bytes]:
        assert len(self._cipher_list) >= 2

        data_list = list(zip(self._AAD_list, self._cipher_list, self._authtag_list))
        H_set = reduce(
            lambda x, y: x & y, 
            [self._calc_possible_H(data_list[i], data_list[i + 1]) for i in range(len(data_list) - 1)]
        )

        return H_set


    def _calc_EJ0(self):
        if self._H is None:
            raise ValueError

        payload = self._merge_ADD_cipher(self._AAD_list[0], self._cipher_list[0])
        H = self._bytes2polynomial(self._H)

        EJ0 = self._bytes2polynomial(self._authtag_list[0]) - sum(
            self._bytes2polynomial(payload[j: j + 16]) * (H ** ((len(payload) - j) // 16))
            for j in range(0, len(payload), 16)
        )

        return self._polynomial2bytes(EJ0)


    def check(self) -> bool:
        if len(self._cipher_list) < 2:
            return False

        if self._H:
            return True

        H_set = self._calc_H()
        if len(H_set) != 1:
            return False

        self._H = H_set.pop()
        self._EJ0 = self._calc_EJ0()
        return True


    def get_H(self) -> bytes:
        return self._H


    def get_EJ0(self) -> bytes:
        return self._EJ0


    def calc_authtag(self, AAD: bytes, cipher: bytes) -> bytes:

        payload = self._merge_ADD_cipher(AAD, cipher)
        H = self._bytes2polynomial(self._H)
        
        authtag_poly = sum(
            self._bytes2polynomial(payload[j: j + 16]) * (H ** ((len(payload) - j) // 16))
            for j in range(0, len(payload), 16)
        ) + self._bytes2polynomial(self._EJ0)

        return self._polynomial2bytes(authtag_poly)


