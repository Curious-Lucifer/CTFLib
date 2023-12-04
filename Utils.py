from pwn import *
from Crypto.Util.number import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']


def local(binary: str, libc: str):
    """
    - input : `binary (str)`, `libc (str)`
    - output : `r (remote object)`
    """

    return process(binary, env={'LD_PRELOAD': libc})


def nc(command: str):
    """
    - input : `command (str)` , `command`' format like `nc <IP/Domain> <port>`
    - output : `r (remote object)`
    """

    _, target, port = command.split()
    return remote(target, int(port))

