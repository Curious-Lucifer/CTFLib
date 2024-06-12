import requests
from gmpy2 import isqrt, iroot

from ..Utils import info


def factordb(n: int, mode: str = 'mul'):
    '''
    ### Example

    ```py

    ```
    '''

    if mode not in ['mul', 'pow']:
        raise ValueError('`mode` should be either `mul` or `pow`')

    factordb_api_url = 'http://factordb.com/api'

    resp = requests.get(factordb_api_url, params = { 'query': n })
    resp.raise_for_status()

    if mode == 'mul':
        factors = [[int(factor)] * power for factor, power in resp.json()['factors']]
        factors = sum(factors, [])
    elif mode == 'pow':
        factors = [[int(factor), power] for factor, power in resp.json()['factors']]

    return factors


def fermat_factor(n: int):
    '''
    ### Example

    ```py

    ```
    '''

    count = 0
    a = int(isqrt(n)) + 1

    b, is_square = iroot(a ** 2 - n, 2)
    while not is_square:
        count += 1
        if (count % 1000):
            info(f'Fermat Factor : {count} attempts')

        a += 1
        b, is_square = iroot(a ** 2 - n, 2)

    b = int(b)
    return (a - b), (a + b)

