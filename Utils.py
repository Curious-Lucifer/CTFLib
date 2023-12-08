from pwn import *
from Crypto.Util.number import *
from tqdm import trange
from gmpy2 import iroot

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']


def local(binary: str, libc: str = None):
    """
    - input : `binary (str)`, `libc (str)`
    - output : `r (remote object)`
    """

    if libc:
        return process(binary, env={'LD_PRELOAD': libc})
    else:
        return process(binary)


def nc(command: str):
    """
    - input : `command (str)` , `command`' format like `nc <IP/Domain> <port>`
    - output : `r (remote object)`
    """

    _, target, port = command.split()
    return remote(target, int(port))

