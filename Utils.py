from pwn import *
from Crypto.Util.number import *
import json

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

    target, port = command.lstrip('nc ').split()
    return remote(target, int(port))

