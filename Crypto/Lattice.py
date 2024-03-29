from .Utils import *
from ..Tools import flatter


def Merkle_Hellman_knapsack(pubkeys: list[int], c: int):
    """
    - input : `pubkeys (list[int])`, `c (int)`
    - output : `M_list (list[int])` , `pubkeys` * `M_list.T` = `c`
    """

    """
    T = pubkeys (1 x n)
    M (n x 1): 1 stands for take, 0 stands for non-take
    T * M = c

    | 1    0    0    ... 0      0  | | M[0]   |   | M[0]   |
    | 0    1    0    ... 0      0  | | M[1]   |   | M[1]   |
    | 0    0    1    ... 0      0  | | M[2]   | = | M[2]   | = u
    |             ...              | | ...    |   | ...    |
    | 0    0    0    ... 1      0  | | M[n-1] |   | M[n-1] |
    | T[0] T[1] T[2] ... T[n-1] -c | | 1      |   | 0      |

    u.norm() < sqrt(n)
    """
    def method1():
        def check_format(v):
            if v[-1] != 0:
                return False
            valid_nums = [0, 1 if 1 in v else -1]
            for num in v[:-1]:
                if not num in valid_nums:
                    return False
            return True

        def check_sign(v):
            return c == sum(p for n, p in zip(v, pubkeys) if n == 1)

        L = Matrix(len(pubkeys) + 1)
        for i in range(len(pubkeys)):
            L[i, i] = 1
            L[-1, i] = pubkeys[i]
        L[-1, -1] = -c

        RES = L.T.LLL()

        for v in RES:
            if check_format(v):
                if check_sign(v):
                    return v
                else:
                    return -v
        return None

    """
    T = pubkeys (1 x n)
    M (n x 1): 1 stands for take, 0 stands for non-take
    T * M = c
    S = 2 * M - ([1] * n).T (n x 1)
    S : 1 stands for take, -1 stands for non-take

    | 2    0    0    ... 0      1 | | M[0]   |   | S[0]   |
    | 0    2    0    ... 0      1 | | M[1]   |   | S[1]   |
    | 0    0    2    ... 0      1 | | M[2]   | = | S[2]   | = u
    |             ...             | | ...    |   | ...    |
    | 0    0    0    ... 2      1 | | M[n-1] |   | S[n-1] |
    | T[0] T[1] T[2] ... T[n-1] c | | -1     |   | 0      |

    u.norm() = sqrt(n)
    """
    def method2():
        def check_format(v):
            if v[-1] != 0:
                return False
            for num in v[:-1]:
                if not num in [-1, 1]:
                    return False
            return True
        
        def check_sign(v):
            return c == sum(p for n, p in zip(v, pubkeys) if n == 1)

        L = Matrix(len(pubkeys) + 1)
        for i in range(len(pubkeys)):
            L[i, i] = 2
            L[i, -1] = 1
            L[-1, i] = pubkeys[i]
        L[-1, -1] = c

        RES = L.T.LLL()

        for v in RES:
            if check_format(v):
                if check_sign(v):
                    return v
                else:
                    return -v
        return None
    
    print('[\033[1m\033[92m+\033[0m\033[0m] Calculating LLL 1')
    res = method1()
    print('[\033[94m*\033[0m] Calculation completed')
    if res:
        return list(res)[:-1]

    print('[\033[1m\033[92m+\033[0m\033[0m] Calculating LLL 2')
    res = method2()
    print('[\033[94m*\033[0m] Calculation completed')
    return [1 if n == 1 else 0 for n in res[:-1]]


def mul_noise_crt(p_list: list[int], y_list: list[int], a_bit_length: int, r_bit_length: int):
    """
    - input : `p_list (list[int])`, `y_list (list[int])`, `a_bit_length (int)`, `r_bit_length (int)`
        - `r0 * a ≡ y0 (mod p0)` 
        - `r1 * a ≡ y1 (mod p1)` 
        - ...
    - output : `a (int)`
    """
    
    P = reduce(lambda x, y: x * y, p_list)
    lambda_list = [(P // p) * pow(P // p, -1, p) for p in p_list]

    n = len(p_list)
    A = 1 << (a_bit_length + r_bit_length + 1)

    B = Matrix(ZZ, n + 1)
    for i in range(n):
        B[i, i] = A
        B[i, -1] = lambda_list[i] * y_list[i]
    B[-1, -1] = P

    RES = flatter(B)
    for v in RES:
        if all(x > 0 for x in v * sign(v[-1])):
            v *= sign(v[-1])
            sol = [x // A for x in v[:-1]]
            return int(v[-1] // reduce(lcm, sol))

