from gmpy2 import isqrt, iroot

from ..Utils import info


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

