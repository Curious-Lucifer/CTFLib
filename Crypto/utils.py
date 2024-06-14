from functools import reduce

from Crypto.Util.number import getRandomNBitInteger
from gmpy2 import is_prime


def xor(*args) -> bytes:
    '''
    ### Example

    ```py
    a = b'123'
    b = b'456'
    c = b'789'
    d = xor(a, b, c)
    ```
    '''

    return bytes([reduce(lambda i, j : i ^ j, l) for l in zip(*args)])


def fastGetPrime(N: int):
    '''
    ### Example

    ```py

    ```
    '''

    if N < 2:
        raise ValueError("N must be larger than 1")
    
    while True:
        number = getRandomNBitInteger(N) | 1
        if is_prime(number):
            break
    return number


def fastIsPrime(N: int):
    '''
    ### Example

    ```py

    ```
    '''

    return is_prime(N)


def mullist2powlist(mullist: list[int]):
    '''
    ### Example

    ```py

    ```
    '''

    return [(num, mullist.count(num)) for num in set(mullist)]
