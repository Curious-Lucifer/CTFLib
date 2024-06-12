from functools import reduce


def xor(*args) -> bytes:
    """
    ### Example

    ```py
    a = b'123'
    b = b'456'
    c = b'789'
    d = xor(a, b, c)
    ```
    """

    return bytes([reduce(lambda i, j : i ^ j, l) for l in zip(*args)])

