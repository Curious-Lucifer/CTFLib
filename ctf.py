#!/usr/bin/env python3

import argparse

from Commands import Pwn


def main():
    parser = argparse.ArgumentParser(description='CTF Tools')
    subparsers = parser.add_subparsers(dest='category')

    pwn_parser = subparsers.add_parser('pwn')
    Pwn.add_arguments(pwn_parser)

    args = parser.parse_args()

    if args.category == 'pwn':
        Pwn.handle(args, pwn_parser)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
