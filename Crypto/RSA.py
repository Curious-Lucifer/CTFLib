from .Utils import *


def pem2key(pem_filename: str):
    """
    - input : `pem_filename (str)`
    - output : `(n, e) (int, int)`
    """

    key = RSA.importKey(open(pem_filename).read())
    return int(key.n), int(key.e)


def factor_n_with_d(n: int, e: int, d: int):
    """
    - input : `n (int)`, `e (int)`, `d (int)`
    - output : `(p, q) (int, int)` , `p * q = n` and p, q is prime
    """

    for g in range(2, n):
        init_pow = e * d - 1
        while ((init_pow % 2) == 0):
            init_pow //= 2
            root = pow(g, init_pow, n)
            if 1 < gcd(root - 1, n) < n:
                p = gcd(root - 1, n)
                q = n // p
                return p, q
            if root == (n - 1):
                break


def fermat_factor(n: int):
    """
    - input : `n (int)`
    - output : `(p, q) (int, int)`
    """

    a = int(isqrt(n)) + 1
    b = iroot(a ** 2 - n, 2)
    while not b[1]:
        a += 1
        b = iroot(a ** 2 - n, 2)
        print(a)
    b = int(b[0])
    return (a - b), (a + b)


def pollard_algorithm(n: int):
    """
    - input : `n (int)` , n has a factor p that (p - 1)'s large prime factor is really small
    - output : `(p, q) (int, int)` , n's factors
    """

    a = 2
    b = 2
    while True:
        a = int(pow(a, b, n))
        p = int(gcd(a - 1, n))
        if 1 < p < n:
            return p, n // p
        b += 1


def william_algorithm(n: int, B: int=None):
    """
    - input : `n (int)`, `B (int, default None)` , B is the upper bound of (p + 1)'s max prime factor
    - output : `(p, q) (int, int)` , `p * q = n`
    """

    def calc_lucas(a: int, k: int):
        """
        - input : `a (int)`, `k (int)`
        - output : `v1 (int)` , return V_k(a, 1)
        """

        # Init : v1, v2 = V[1], V[2]
        # General : v1, v2 = V[i], V[i + 1]
        v1, v2 = a % n, (a ** 2 - 2) % n
        for bit in bin(k)[3:]:
            if bit == '1':
                # v1, v2 = V[2i + 1], V[2i + 2]
                v1, v2 = (v1 * v2 - a) % n, (v2 ** 2 - 2) % n
            else:
                # v1, v2 = V[2i], V[2i + 1]
                v1, v2 = (v1 ** 2 - 2) % n, (v1 * v2 - a) % n
        return v1

    prime_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    
    B = B or int(isqrt(n))
    for A in prime_list:
        v = A
        for i in trange(1, B + 1, desc=f'A = {A}'):
            v = calc_lucas(v, i)
            p = gcd(v - 2, n)
            if n > p > 1:
                return p, n // p


def wiener_attack(n: int, e: int):
    """
    - input : `n (int)`, `e (int)`
    - output : `(p, q, d) (int, int, int)`
    """

    continued_fraction_list = (Integer(e) / Integer(n)).continued_fraction()
    for i in range(2, len(continued_fraction_list)):
        cf = continued_fraction_list.convergent(i)
        k = cf.numerator()
        d = cf.denominator()
        if ((e * d - 1) % k) != 0:
            continue
        b = (e * d - 1) // k - n - 1
        if (b ** 2 - 4 * n) <= 0:
            continue
        D = iroot(int(b ** 2 - 4 * n), 2)
        if not D[1]:
            continue
        p, q = ((-int(b) + int(D[0])) // 2), ((-int(b) - int(D[0])) // 2)
        if p * q == n:
            return p, q, int(d)


def LSB_oracle_attack(n: int, e: int, c: int, oracle, m_bitlength: int = None):
    """
    - input : `n (int)`, `e (int)`, `c (int)`, `oracle (func)`, `m_bitlength (int, default = None)`
    - output : `m (int)`
    - oracle func : 
        - input : `c (int)`
        - output : `lbit (int)` , `{0, 1}` last bit of `m` (`c`'s plain)
    """

    m_bitlength = m_bitlength or n.bit_length()
    multiple_const = pow(2, -e, n)
    m_bitlist = []
    for i in trange(m_bitlength):
        new_c = (pow(multiple_const, i, n) * c) % n
        bit = (oracle(new_c) - (sum((pow(2, - i + j, n) * m_bitlist[j] % n) for j in range(i)) % n)) % 2
        m_bitlist.append(bit)

    return int(''.join(str(bit) for bit in reversed(m_bitlist)), base=2)


def bleichenbacher_1998(n: int, e: int, c: int, oracle):
    """
    - input : `n (int)`, `e (int)`, `c (int)`, `oracle (func)` , `c` is PKCS#1 conforming
    - output : `m (int)` , `c`'s plain
    - oracle func : 
        - input : `c (int)`
        - output : `PKCS_conforming (bool)` , is `c` PKCS#1 conforming
    """

    assert oracle(c)
    B = 1 << (n.bit_length() // 8 - 1) * 8

    def bleichenbacher_orifind_s(lower_bound: int):
        si = lower_bound
        while True:
            new_c = (pow(si, e, n) * c) % n
            if oracle(new_c):
                return si
            si += 1

    def bleichenbacher_optfind_s(prev_si: int, a: int, b: int):
        ri = ceil_int(2 * (b * prev_si - 2 * B), n)
        while True:
            low_bound = ceil_int(2 * B + ri * n, b)
            high_bound = ceil_int(3 * B + ri * n, a)
            for si in range(low_bound, high_bound):
                new_c = (pow(si, e, n) * c) % n
                if oracle(new_c):
                    return si
            ri += 1

    def bleichenbacher_merge_M(si: int, M: list):
        new_M = []
        for [a, b] in M:
            r_low = ceil_int(a * si - 3 * B + 1, n)
            r_high = floor_int(b * si - 2 * B, n) + 1
            for ri in range(r_low, r_high):
                interval_low = max(a, ceil_int(2 * B + ri * n, si))
                interval_high = min(b, floor_int(3 * B + ri * n - 1, si))
                if interval_high >= interval_low:
                    new_M.append([interval_low, interval_high])
        return new_M

    s = bleichenbacher_orifind_s(ceil_int(n, 3 * B))
    M = bleichenbacher_merge_M(s, [[2 * B, 3 * B - 1]])
    print(s, M)

    while True:
        if len(M) > 1:
            s = bleichenbacher_orifind_s(s + 1)
        else:
            if M[0][0] == M[0][1]:
                return M[0][0]
            s = bleichenbacher_optfind_s(s, M[0][0], M[0][1])
        M = bleichenbacher_merge_M(s, M)
        print(s, M)


def stereotyped_message(n: int, e: int, c: int, m0: int, epsilon=None):
    """
    - input : `n (int)`, `e (int)`, `c (int)`, `m0 (int)`, `epsilon (default=None)` , `0 < epsilon <= 1/7`
    - output : `m (int)` , `c`'s plain. if there's no solve, return `-1`
    """
    P = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]

    f = (m0 + x) ** e - c
    small_roots = f.small_roots(epsilon=epsilon)
    if len(small_roots) > 0:
        return int(small_roots[0]) + m0
    else:
        return -1


def known_high_bits_of_p(n: int, p0: int, epsilon=None):
    """
    - input : `n (int)`, `p0 (int)`, `epsilon (default=None)` , `0 < epsilon <= 0.5/7`
    - output : `(p, q) (int, int)`
    """
    P = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]
    
    f = p0 + x
    small_roots = f.small_roots(beta=0.5, epsilon=epsilon)
    if len(small_roots) > 0:
        p = p0 + int(small_roots[0])
        q = n // p
        assert p * q == n
        return p, q
    else:
        return -1


def broadcast_with_linear(a_list: list[int], b_list: list[int], c_list: list[int], n_list: list[int], e: int, epsilon=None):
    """
    - input : `a_list (list[int])`, `b_list (list[int])`, `c_list (list[int])`, `n_list (list[int])`, `e (int)`, `epsilon (default=None)` , `0 < epsilon <= 1/7`
        - `(a1 * m + b1) ^ e ≡ c1 (mod n1)
        - `(a2 * m + b2) ^ e ≡ c2 (mod n2)
        - ...
    - output : `m % N (int)` , `N = n1 * n2 * ...`
    """

    N = reduce(lambda x, y: x * y, n_list)
    t_list = []
    for i in range(e):
        ai_list = [0] * e
        ai_list[i] = 1
        t_list.append(crt(ai_list, n_list))

    P = PolynomialRing(Zmod(N), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]

    g = 0
    for i in range(e):
        f = a_list[i] * x + b_list[i]
        g += t_list[i] * (f ** e - c_list[i])

    g *= pow(int(g.leading_coefficient()), -1, N)
    small_roots = g.small_roots(epsilon=epsilon)
    if len(small_roots) > 0:
        return int(small_roots[0])
    else:
        return -1


def franklin_reiter(e: int, c1: int, c2: int, f, x):
    """
    - input : `e (int)`, `c1 (int)`, `c2 (int)`, `f (polynomial of x mod n)`, `x (symbol of polynomial mod n)`
    - output : `m1 (int)` , `f(m1) = m2`

    `f` & `x`'s example : 
    ```python
    P = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]
    f = x ** 6 + 3 * x ** 5 + 17 * x ** 4 + 2 * x ** 3 + x ** 2 + 7 * x + 79
    ```
    """

    f1 = x ** e - c1
    f2 = f ** e - c2
    return int(-polynomialgcd(f1, f2)[0])


def coppersmith_short_pad_attack(n: int, e: int, c1: int, c2: int, epsilon=None):
    """
    - input : `n (int)`, `e (int)`, `c1 (int)`, `c2 (int)`, `epsilon (default=None)` , `0 < epsilon <= 1/7`
    - output : `m1 (int)` , `c1`'s plain
    """

    P2 = PolynomialRing(IntegerRing(), names=('x', 'y'))
    (x, y) = P2._first_ngens(2)

    f1 = x ** e - c1
    f2 = (x + y) ** e - c2
    h = f1.resultant(f2, x).univariate_polynomial().change_ring(Zmod(n))
    small_roots = h.small_roots(epsilon=epsilon)
    if len(small_roots) > 0:
        diff = small_roots[0]
    else:
        return -1

    P = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    x = P._first_ngens(1)[0]

    f = x + diff
    return franklin_reiter(e, c1, c2, f, x)


def small_roots(f, bounds, m , d):
    """
    > Ref : https://github.com/defund/coppersmith
    """

    R = f.base_ring()
    N = R.cardinality()

    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ** (m - i) * f ** i
        for shifts in product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)

    B = B.dense_matrix().LLL()

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)

    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1 :
            H.pop()
        elif I.dimension() == 0 :
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots

    return []


def boneh_durfee(e: int, n: int, delta: float=0.262, m: int=3, d: int=4):
    """
    - input : `e (int)`, `n (int)`, `delta (float, default=0.262)`, `m (int, default=3)`, `d (int, default=4)` , `d < n ** delta`
    - output : `p, q, d (int, int, int)`

    > Ref : https://github.com/defund/coppersmith
    """

    bounds = (floor(n ** RealNumber(delta)), 1 << ((n.bit_length() // 2) + (n.bit_length() % 2)))

    R = Integers(e)
    P = PolynomialRing(R, names=('k', 's',))
    (k, s,) = P._first_ngens(2)

    f = 2 * k * ((n + 1) // 2 - s) + 1

    try:
        # (e * d - 1) // ((p - 1) * (q - 1)), (p + q) // 2
        _, p_plus_q = small_roots(f, bounds, m=m, d=d)[0]
        p_plus_q = int(p_plus_q) * 2
    except:
        return -1, -1, -1
    
    D = p_plus_q ** 2 - 4 * n
    p = (p_plus_q + int(isqrt(D))) // 2
    q = (p_plus_q - int(isqrt(D))) // 2
    d = pow(e, -1, (p - 1) * (q - 1))
    return p, q, d

