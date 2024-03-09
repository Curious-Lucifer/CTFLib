from typing import Union
import shutil

from .pwntools_import import process, remote, info, success


def local(binary: Union[str, list[str]], libc: str = None):
    if libc:
        return process(binary, env={'LD_PRELOAD': libc})
    return process(binary)


def nc(command: str):
    target, port = command.lstrip('nc').split()
    return remote(target, int(port))


def check_command(command: str) -> bool:
    return shutil.which(command) is not None

