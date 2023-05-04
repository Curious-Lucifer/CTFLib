
def length_extension_attack(digest: bytes, known_data: bytes, data_to_add: bytes, unknown_data_length: int):
    """
    - input : `digest (bytes)`, `knonw_data (bytes)`, `data_to_add (bytes)`, `unknown_data_length (int)`
    - output : `(new_digest, new_known_data) (bytes, bytes)`
    """
    
    if len(digest) == 16:
        hash_mode = 'md5'
        chunk_size = 64
    if len(digest) == 20:
        hash_mode = 'sha1'
        chunk_size = 64
    if len(digest) == 32:
        hash_mode = 'sha256'
        chunk_size = 64
    if len(digest) == 64:
        hash_mode = 'sha512'
        chunk_size = 128

    ori_data_length = unknown_data_length + len(known_data)
    new_known_data = known_data + hash_pad(ori_data_length, hash_mode) + data_to_add

    data_to_add += hash_pad(unknown_data_length + len(new_known_data), hash_mode)
    for chunk in [data_to_add[i: i + chunk_size] for i in range(0, len(data_to_add), chunk_size)]:
        digest = hash_chunk(digest, chunk, hash_mode)

    return digest, new_known_data


def hash_pad(data_length: int, hash_mode: str):
    if hash_mode == 'md5':
        null_pad_length = (56 - data_length - 1) % 64
        return b'\x80' + b'\x00' * null_pad_length + (data_length * 8).to_bytes(8, byteorder='little')
    if hash_mode == 'sha1':
        null_pad_length = (56 - data_length - 1) % 64
        return b'\x80' + b'\x00' * null_pad_length + (data_length * 8).to_bytes(8, byteorder='big')
    if hash_mode == 'sha256':
        null_pad_length = (56 - data_length - 1) % 64
        return b'\x80' + b'\x00' * null_pad_length + (data_length * 8).to_bytes(8, byteorder='big')
    if hash_mode == 'sha512':
        null_pad_length = (120 - data_length - 1) % 128
        return b'\x80' + b'\x00' * null_pad_length + (data_length * 8).to_bytes(8, byteorder='big')


def hash_chunk(digest: bytes, chunk: bytes, hash_mode: str):
    if hash_mode == 'md5':
        return md5_chunk(digest, chunk)
    if hash_mode == 'sha1':
        return sha1_chunk(digest, chunk)
    if hash_mode == 'sha256':
        return sha256_chunk(digest, chunk)
    if hash_mode == 'sha512':
        return sha512_chunk(digest, chunk)


def md5_chunk(digest: bytes, chunk: bytes):
    [h0, h1, h2, h3] = [int.from_bytes(digest[i: i + 4], byteorder='little') for i in range(0, len(digest), 4)]

    R = [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
    ]
    K = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 
        0xd62f105d, 0x2441453,  0xd8a1e681, 0xe7d3fbc8, 
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
    ]

    left_rotate = lambda x, n: (x << n | x >> (32 - n)) & 0xFFFFFFFF
    modular_add = lambda *args : sum(args) & 0xFFFFFFFF

    w = [int.from_bytes(chunk[i: i + 4], byteorder='little') for i in range(0, len(chunk), 4)]
    a, b, c, d = h0, h1, h2, h3

    for i in range(64):
        if 0 <= i < 16:
            f = (b & c) | (~b & d)
            g = i
        elif 16 <= i < 32:
            f = (d & b) | (~d & c)
            g = (5 * i + 1) % 16
        elif 32 <= i < 48:
            f = b ^ c ^ d
            g = (3 * i + 5) % 16
        else:
            f = c ^ (b | ~d)
            g = (7 * i) % 16

        a, b, c, d = d, modular_add(left_rotate(modular_add(a, f, K[i], w[g]), R[i]), b), b, c

    h0 = modular_add(h0, a)
    h1 = modular_add(h1, b)
    h2 = modular_add(h2, c)
    h3 = modular_add(h3, d)

    return b''.join(int.to_bytes(h, 4, byteorder='little') for h in (h0, h1, h2, h3))


def sha1_chunk(digest: bytes, chunk: bytes):
    [h0, h1, h2, h3, h4] = [int.from_bytes(digest[i: i + 4], byteorder='big') for i in range(0, len(digest), 4)]

    left_rotate = lambda x, n: (x << n | x >> (32 - n)) & 0xFFFFFFFF
    modular_add = lambda *args : sum(args) & 0xFFFFFFFF
    
    w = [int.from_bytes(chunk[i: i + 4], byteorder='big') for i in range(0, len(chunk), 4)]
    for i in range(16, 80):
        w.append(left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))

    a, b, c, d, e = h0, h1, h2, h3, h4
    for i in range(80):
        if 0 <= i < 20:
            f = (b & c) | (~b & d)
            k = 0x5A827999
        elif 20 <= i < 40:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i < 60:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        a, b, c, d, e = modular_add(left_rotate(a, 5), f, e, k, w[i]), a, left_rotate(b, 30), c, d

    h0 = modular_add(h0, a)
    h1 = modular_add(h1, b)
    h2 = modular_add(h2, c)
    h3 = modular_add(h3, d)
    h4 = modular_add(h4, e)

    return b''.join(int.to_bytes(h, 4, byteorder='big') for h in (h0, h1, h2, h3, h4))


def sha256_chunk(digest: bytes, chunk: bytes):
    [h0, h1, h2, h3, h4, h5, h6, h7] = [int.from_bytes(digest[i: i + 4], byteorder='big') for i in range(0, len(digest), 4)]

    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    right_rotate = lambda x, n: (x << (32 - n) | x >> n) & 0xFFFFFFFF
    modular_add = lambda *args : sum(args) & 0xFFFFFFFF

    w = [int.from_bytes(chunk[i: i + 4], byteorder='big') for i in range(0, len(chunk), 4)]
    for i in range(16, 64):
        s0 = right_rotate(w[i - 15], 7) ^ right_rotate(w[i - 15], 18) ^ (w[i - 15] >> 3)
        s1 = right_rotate(w[i - 2], 17) ^ right_rotate(w[i - 2], 19) ^ (w[i - 2] >> 10)
        w.append(modular_add(w[i - 16], w[i - 7], s0, s1))

    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    f = h5
    g = h6
    h = h7
    for i in range(64):
        s1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
        ch = (e & f) ^ (~e & g)
        temp1 = modular_add(h, s1, ch, k[i], w[i])
        s0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = modular_add(s0, maj)

        h = g
        g = f
        f = e
        e = modular_add(d, temp1)
        d = c
        c = b
        b = a
        a = modular_add(temp1, temp2)

    h0 = modular_add(h0, a)
    h1 = modular_add(h1, b)
    h2 = modular_add(h2, c)
    h3 = modular_add(h3, d)
    h4 = modular_add(h4, e)
    h5 = modular_add(h5, f)
    h6 = modular_add(h6, g)
    h7 = modular_add(h7, h)

    return b''.join(int.to_bytes(h, 4, byteorder='big') for h in (h0, h1, h2, h3, h4, h5, h6, h7))


def sha512_chunk(digest: bytes, chunk: bytes):
    [h0, h1, h2, h3, h4, h5, h6, h7] = [int.from_bytes(digest[i: i + 8], byteorder='big') for i in range(0, len(digest), 8)]

    k = [
        0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538, 
        0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe, 
        0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 
        0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 
        0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab, 
        0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725, 
        0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 
        0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b, 
        0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218, 
        0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 
        0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 
        0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec, 
        0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c, 
        0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6, 
        0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 
        0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
    ]

    right_rotate = lambda x, n: (x << (64 - n) | x >> n) & 0xFFFFFFFFFFFFFFFF
    modular_add = lambda *args : sum(args) & 0xFFFFFFFFFFFFFFFF

    w = [int.from_bytes(chunk[i: i + 8], byteorder='big') for i in range(0, len(chunk), 8)]
    for i in range(16, 80):
        s0 = right_rotate(w[i - 15], 1) ^ right_rotate(w[i - 15], 8) ^ (w[i - 15] >> 7)
        s1 = right_rotate(w[i - 2], 19) ^ right_rotate(w[i - 2], 61) ^ (w[i - 2] >> 6)
        w.append(modular_add(w[i - 16], w[i - 7], s0, s1))

    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    f = h5
    g = h6
    h = h7
    for i in range(80):
        s1 = right_rotate(e, 14) ^ right_rotate(e, 18) ^ right_rotate(e, 41)
        ch = (e & f) ^ (~e & g)
        temp1 = modular_add(h, s1, ch, k[i], w[i])
        s0 = right_rotate(a, 28) ^ right_rotate(a, 34) ^ right_rotate(a, 39)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = modular_add(s0, maj)

        h = g
        g = f
        f = e
        e = modular_add(d, temp1)
        d = c
        c = b
        b = a
        a = modular_add(temp1, temp2)

    h0 = modular_add(h0, a)
    h1 = modular_add(h1, b)
    h2 = modular_add(h2, c)
    h3 = modular_add(h3, d)
    h4 = modular_add(h4, e)
    h5 = modular_add(h5, f)
    h6 = modular_add(h6, g)
    h7 = modular_add(h7, h)

    return b''.join(int.to_bytes(h, 8, byteorder='big') for h in (h0, h1, h2, h3, h4, h5, h6, h7))
