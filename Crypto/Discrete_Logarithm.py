from .Utils import *


def giant_baby(gi: int, hi: int, p: int, pi: int=None):
    """
    - input : `gi (int)`, `hi (int)`, `p (int)`, `pi (int, default=None)`
        - `g ^ (((p - 1) / pi) * x) ≡ h ^ ((p - 1) / pi) (mod p)`
        - `gi ≡ g ^ ((p - 1) / pi) (mod p)`
        - `hi ≡ h ^ ((p - 1) / pi) (mod p)`
    - output : `x (int)` , `x (mod pi)` or `x (mod (p - 1))`
    """

    pi = pi or p - 1

    giant = {}
    sqrt = int(isqrt(pi)) + 1

    gs, gks = pow(gi, sqrt, p), 1
    for k in trange(sqrt, leave=False, desc="Giant"):
        giant[gks] = k
        gks = gks * gs % p

    for i in trange(sqrt, leave=False, desc="Baby"):
        try:
            k = giant[hi]
            return (k * sqrt - i) % pi
        except KeyError:
            hi = hi * gi % p


def Pollard_rho(gi: int, hi: int, p: int, pi: int):
    """
    - input : `gi (int)`, `hi (int)`, `p (int)`, `pi (int)`
        - `g ^ (((p - 1) / pi) * x) ≡ h ^ ((p - 1) / pi) (mod p)`
        - `gi ≡ g ^ ((p - 1) / pi) (mod p)`
        - `hi ≡ h ^ ((p - 1) / pi) (mod p)`
    - output : `x (int)` , `x (mod pi)`
    """

    assert isPrime(pi)

    def new(x: int, a: int, b: int):
        if x % 3 == 1:
            return (x * gi % p, (a + 1) % pi, b)
        if x % 3 == 2:
            return (x * hi % p, a, (b + 1) % pi)
        return (x * x % p, 2 * a % pi, 2 * b % pi)
    
    if gi == hi:
        return 1
    
    x1, a1, b1 = 1, 0, 0
    x2, a2, b2 = 1, 0, 0
    for _ in trange(pi, leave=False):
        x1, a1, b1 = new(x1, a1, b1)
        x2, a2, b2 = new(x2, a2, b2)
        x2, a2, b2 = new(x2, a2, b2)
        if x1 == x2:
            return ((a2 - a1) * pow(b1 - b2, -1, pi)) % pi


def Pohlig_Hellman(g: int, h: int, p: int, factor_list: list[tuple[int, int]], discrete_log_func=giant_baby):
    """
    - input : `g (int)`, `h (int)`, `p (int)`, `factor_list (list[tuple[int, int]])`, `discrete_log_func (func, default=giant_baby)`
    - outupt : `x (int)` , `x (mod (p - 1))`
    - discrete_log_func : 
        - input : `gi (int)`, `hi (int)`, `p (int)`, `pi (int)`
            - `g ^ (((p - 1) / pi) * x) ≡ h ^ ((p - 1) / pi) (mod p)`
            - `gi ≡ g ^ ((p - 1) / pi) (mod p)`
            - `hi ≡ h ^ ((p - 1) / pi) (mod p)`
        - output : `x (int)` , `x (mod pi)`
    """

    x_list = []
    pi_list = []
    for pi, time in factor_list:
        if time == 1:
            gi = pow(g, (p - 1) // pi, p)
            hi = pow(h, (p - 1) // pi, p)
            x_list.append(discrete_log_func(gi, hi, p, pi))
            pi_list.append(pi)
        else:
            gi = pow(g, (p - 1) // pi, p)
            xi = 0
            for i in range(time):
                hi = pow(h * pow(g, -xi, p), (p - 1) // (pi ** (i + 1)), p)
                xi += discrete_log_func(gi, hi, p, pi) * (pi ** i)
            x_list.append(xi)
            pi_list.append(pi ** time)

    return crt(x_list, pi_list)

