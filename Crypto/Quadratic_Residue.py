from .Utils import *


def Tonelli_Shanks(a: int, p: int, time: int=1):
    """
    - input : `a (int)`, `p (int)`, `time (int, default=1)`
    - output : `r0, r1 (int, int)` , `r0 ** 2 ≡ a (mod p ** time)` && `r1 ** 2 ≡ a (mod p ** time)`
    """

    isPrime = time == 1
    pt = p ** time

    if (a % (pt)) == 0:
        return 0, 0

    if isPrime:
        assert legendre_symbol(a, p) == 1

        if (p % 4) == 3:
            r = pow(a, (p + 1) // 4, p)
            return r, -r % p

    Q, S = (p - 1) * (p ** (time - 1)), 0
    while (Q % 2) == 0:
        Q //= 2
        S += 1

    z = 2
    if isPrime:
        while legendre_symbol(z, p) != -1:
            z += 1
    else:
        assert time % 2 == 1, "Can't find quadratic nonresidue"
        while jocobi_symbol(z, [(p, time)]) != -1:
            z += 1

    M, c, t, R = S, pow(z, Q, pt), pow(a, Q, pt), pow(a, (Q + 1) // 2, pt)
    while True:
        if t == 1:
            return R, -R % pt
        
        i = 1
        while pow(t, 1 << i, pt) != 1:
            i += 1

        b = pow(c, 1 << (M - i - 1), pt)
        M, c, t, R = i, pow(b, 2, pt), (t * pow(b, 2, pt)) % pt, (R * b) % pt


def quadratic_residue(a: int, factor_list: list[tuple[int, int]]):
    """
    - input : `a (int)`, `factor_list (list[tuple[int, int]])`
    - output : `r_list (list[int])`
    """

    r_possible_list = []
    p_list = []
    for factor, time in factor_list:
        r_possible_list.append(tuple(set(Tonelli_Shanks(a, factor, time))))
        p_list.append(factor ** time)

    res_list = []
    for r_list in product(*r_possible_list):
        res_list.append(crt(r_list, p_list))
    
    return list(set(res_list))

