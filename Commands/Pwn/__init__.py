import argparse

from . import get_libc
from . import get_shell
from . import get_vmlinux


def add_arguments(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest='cmd')
    
    get_libc_parser = subparsers.add_parser('get-libc')
    get_libc.add_arguments(get_libc_parser)

    get_vmlinux_parser = subparsers.add_parser('get-vmlinux')
    get_vmlinux.add_arguments(get_vmlinux_parser)

    get_shell_parser = subparsers.add_parser('get-shell')
    get_shell.add_arguments(get_shell_parser)


def handle(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if args.cmd == 'get-libc':
        get_libc.handle(args)
    elif args.cmd == 'get-vmlinux':
        get_vmlinux.handle(args)
    elif args.cmd == 'get-shell':
        get_shell.handle(args)
    else:
        parser.print_help()

