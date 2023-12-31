from .Utils import *


class SimpleEllipticCurve:
    def __init__(self, a: int, b: int, p: int):
        """
        - input : `a (int)`, `b (int)`, `p (int)` , `y ** 2 ≡ x ** 3 + a * x + b (mod p)`
        """

        self.a, self.b, self.p = a, b, p

    def __str__(self):
        return f'y ** 2 ≡ x ** 3 + {self.a} * x + {self.b} (mod {self.p})'

    def __eq__(self, other):
        assert isinstance(other, self.__class__)

        return (self.a == other.a) and (self.b == other.b) and (self.p == other.p)

    def point(self, x: int, y: int):
        return SimpleEllipticCurve_Point(x, y, self)


class SimpleEllipticCurve_Point:
    def __init__(self, x: int, y: int, curve: SimpleEllipticCurve):
        """
        - input : `x (int)`, `y (int)`, `curve (EllipticCurve)`
        """

        self.curve = curve
        self.p = curve.p
        self.x, self.y= x % self.p, y % self.p


    def __copy__(self):
        return self.__class__(self.x, self.y, self.curve)

    def __str__(self):
        return f'({self.x}, {self.y}) on ({self.curve})'

    def __eq__(self, other):
        assert isinstance(other, self.__class__) and (self.curve == other.curve)

        return (self.x == other.x) and (self.y == other.y) and (self.curve == other.curve)

    def __neg__(self):
        return self.__class__(self.x, -self.y, self.curve)

    def __add__(self, other):
        assert isinstance(other, self.__class__) and (self.curve == other.curve)

        if (self.x == 0) and (self.y == 0) :
            return other.__copy__()
        if (other.x == 0) and (other.y == 0):
            return self.__copy__()
        
        if self == -other:
            return self.__class__(0, 0, self.curve)
        
        if self == other:
            m = (3 * pow(self.x, 2, self.p) + self.curve.a) * pow(2 * self.y, -1, self.p) % self.p
        else:
            m = (other.y - self.y) * pow(other.x - self.x, -1, self.p) % self.p

        x = pow(m, 2, self.p) - self.x - other.x
        y = m * (self.x - x) - self.y

        return self.__class__(x, y, self.curve)

    def __mul__(self, other: int):
        return self.__rmul__(other)

    def __rmul__(self, other: int):
        assert isinstance(other, int)

        Q, R = self.__copy__(), self.__class__(0, 0, self.curve)
        while other > 0:
            if (other % 2) == 1:
                R = R + Q
            Q, other = Q + Q, other // 2
        return R


def ECC_Pohlig_Hellman(G, H, order: int, factor_list: list[tuple[int, int]]):
    """
    - input : `G`, `H`, `order (int)`, `factor_list (list[tuple[int, int]])`
    - output : `n (int)` , `H = n * G`

    `G` & `H` & `order`'s example : 
    ```python
    curve = EllipticCurve(GF(p), [a, b])
    order = curve.order()
    G, H = curve(Gx, Gy), curve(Hx, Hy)
    ```
    """

    n_list = []
    pi_list = []
    for pi, time in tqdm(factor_list, leave=False):
        Gi, Hi = (order // (pi ** time)) * G, (order // (pi ** time)) * H
        n_list.append(int(discrete_log(Hi, Gi, operation='+')))
        pi_list.append(pi ** time)

    return crt(n_list, pi_list)

