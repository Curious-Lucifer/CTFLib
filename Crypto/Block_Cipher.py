from .Utils import *
from Crypto.Util.number import bytes_to_long, long_to_bytes


def padding_oracle_attack(pre_cipher_block: bytes, cipher_block: bytes, oracle):
    '''
    - input : `pre_cipher_block (bytes)`, `cipher_block (bytes)`, `oracle (func)`
    - output : `plain_block (bytes)` , cipher_block's plaintext
    - oracle func : 
        - input : `cipher (bytes)`
        - output : `padding_right (bool)` , represent if the padding of cipher's plaintext is right
    '''

    assert len(pre_cipher_block) == len(cipher_block) == 16

    last_bytes = []
    for i in range(256):
        cipher_test = pre_cipher_block[:15] + bytes([i]) + cipher_block
        if oracle(cipher_test):
            last_bytes.append(bytes([i]))
    if len(last_bytes) == 1:
        plain_block = xor(last_bytes[0], b'\x01', pre_cipher_block[-1:])
    else:
        plain_block = xor(last_bytes[last_bytes.index(pre_cipher_block[-1:]) ^ 1], b'\x01', pre_cipher_block[-1:])
    print(str(plain_block), end='\r')

    for j in range(1,16):
        for i in range(256):
            cipher_test = pre_cipher_block[:15 - j] + bytes([i]) + xor(pre_cipher_block[-j:], plain_block, bytes([j + 1]) * j) + cipher_block
            if oracle(cipher_test):
                plain_block = xor(bytes([i]), bytes([j + 1]), pre_cipher_block[-j - 1:-j]) + plain_block
                break
        print(str(plain_block), end='\r')
    print(f'result : {str(plain_block)}')

    return plain_block


class GCM_Forbidden_Attack:
    """
    - method
        - `append` : add new `AAD`, `cipher`, `auth_tag` to the instance (their nonce and key need to be the same)
        - `calc_H` : calc the posible `H` for the data in the instance
        - `calc_EJ0` : use `H` to calc the corresponding `EJ0`
    - class method
        - `calc_auth_tag` : use the `H`(represent the same key), `EJ0`(respresent the same nonce) to calc `auth_tag` for new `AAD` and `cipher`
    """

    x = var('x')
    K = GF(2 ** 128, name='a', modulus=x ** 128 + x ** 7 + x ** 2 + x + 1, names=('a',))
    P = PolynomialRing(K, names=('x',))

    a = K._first_ngens(1)[0]
    x = P._first_ngens(1)[0]


    def __init__(self, AAD_list: list[bytes]=[], cipher_list: list[bytes]=[], auth_tag_list: list[bytes]=[]):
        """
        - input
            - `AAD_list (list[bytes], [AAD1, AAD2, ...])`
            - `cipher_list (list[bytes], [cipher1, cipher2, ...])`
            - `auth_tag_list (list[bytes], [auth_tag1, auth_tag2, ...])`
        """

        self.AAD_list = AAD_list
        self.cipher_list = cipher_list
        self.auth_tag_list = auth_tag_list


    def append(self, AAD: bytes, cipher: bytes, auth_tag: bytes):
        """
        - input : `AAD (bytes)`, `cipher (bytes)`, `auth_tag (bytes)`
        """

        self.AAD_list.append(AAD)
        self.cipher_list.append(cipher)
        self.auth_tag_list.append(auth_tag)


    @staticmethod
    def bytes2polynomial(bytes_string: bytes):
        """
        - input : `bytes_string (bytes, 16 bytes)`
        - output : `polynomial` , polynomial of `a` that in `GF(2 ** 128, name='a', modulos=y ** 128 + y ** 7 + y ** 2 + y + 1, names=('a',))`
        """

        assert len(bytes_string) == 16

        bin_bytes_string = bin(bytes_to_long(bytes_string))[2:].rjust(128, '0')
        return sum(int(bit) * GCM_Forbidden_Attack.a ** i for i, bit in enumerate(bin_bytes_string))


    @staticmethod
    def polynomial2bytes(polynomial):
        """
        - input : `polynomial` , polynomial of `a` that in `GF(2 ** 128, name='a', modulos=y ** 128 + y ** 7 + y ** 2 + y + 1, names=('a',))`
        - output : `bytes_string (bytes, 16 bytes)`
        """

        term_list = str(polynomial).split(' + ')
        bin_list = ['0'] * 128

        if '1' in term_list:
            bin_list[0] = '1'
            term_list.pop(-1)

        if 'a' in term_list:
            bin_list[1] = '1'
            term_list.pop(-1)

        for term in term_list:
            bin_list[int(term.split('^')[1])] = '1'

        return long_to_bytes(int(''.join(bin_list), base=2), 16)


    @staticmethod
    def merge_AAD_cipher(AAD: bytes, cipher: bytes):
        '''
        - input : `AAD (bytes)`, `cipher (bytes)`
        - output : `payload (bytes)`
        '''
        
        payload = AAD
        if (len(payload) % 16) != 0:
            payload += b'\x00' * (16 - len(payload) % 16)

        payload += cipher
        if (len(payload) % 16) != 0:
            payload += b'\x00' * (16 - len(payload) % 16)

        return payload + long_to_bytes(len(AAD) * 8, 8) + long_to_bytes(len(cipher) * 8, 8)


    def calc_H(self):
        """
        - input : `None`
        - output : `H_list (list[bytes])` , [H1, H2, ...] and one of it is the real H
        """

        for i in range(len(self.cipher_list) - 1):
            payload1 = GCM_Forbidden_Attack.merge_AAD_cipher(self.AAD_list[i], self.cipher_list[i])
            payload2 = GCM_Forbidden_Attack.merge_AAD_cipher(self.AAD_list[i + 1], self.cipher_list[i + 1])

            poly1 = sum(GCM_Forbidden_Attack.bytes2polynomial(payload1[j * 16: (j + 1) * 16]) * (GCM_Forbidden_Attack.x ** (len(payload1) // 16 - j)) for j in range(len(payload1) // 16))
            poly2 = sum(GCM_Forbidden_Attack.bytes2polynomial(payload2[j * 16: (j + 1) * 16]) * (GCM_Forbidden_Attack.x ** (len(payload2) // 16 - j)) for j in range(len(payload2) // 16))

            f = poly1 - poly2 + GCM_Forbidden_Attack.bytes2polynomial(self.auth_tag_list[i + 1]) - GCM_Forbidden_Attack.bytes2polynomial(self.auth_tag_list[i])
            root_list = [GCM_Forbidden_Attack.polynomial2bytes(root) for root, _ in f.roots()]

            if i == 0:
                H_list = set(root_list)
            else:
                H_list &= set(root_list)

        return list(H_list)


    def calc_EJ0(self, H: bytes):
        """
        - input : `H (bytes)`
        - output : `EJ0 (bytes)`
        """

        payload = GCM_Forbidden_Attack.merge_AAD_cipher(self.AAD_list[0], self.cipher_list[0])
        H = GCM_Forbidden_Attack.bytes2polynomial(H)
        EJ0 = GCM_Forbidden_Attack.bytes2polynomial(self.auth_tag_list[0]) - sum(GCM_Forbidden_Attack.bytes2polynomial(payload[j * 16: (j + 1) * 16]) * (H ** (len(payload) // 16 - j)) for j in range(len(payload) // 16))
        return GCM_Forbidden_Attack.polynomial2bytes(EJ0)


    @classmethod
    def calc_auth_tag(cls, H: bytes, EJ0: bytes, AAD: bytes, cipher: bytes):
        """
        - input : `H (bytes)`, `EJ0 (bytes)`, `AAD (bytes)`, `cipher (bytes)`
        - output : `auth_tag (bytes)` , (AAD & cipher)'s auth tag
        """

        payload = cls.merge_AAD_cipher(AAD, cipher)
        H = cls.bytes2polynomial(H)

        auth_tag_poly = sum(cls.bytes2polynomial(payload[j * 16: (j + 1) * 16]) * (H ** (len(payload) // 16 - j)) for j in range(len(payload) // 16))
        auth_tag_poly += cls.bytes2polynomial(EJ0)

        return cls.polynomial2bytes(auth_tag_poly)

