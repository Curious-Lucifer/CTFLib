import argparse

from . import get_libc


def add_arguments(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest='cmd')
    
    get_libc_parser = subparsers.add_parser('get-libc')
    get_libc.add_arguments(get_libc_parser)


def handle(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if args.cmd == 'get-libc':
        get_libc.handle(args)
    else:
        parser.print_help()

