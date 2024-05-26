import argparse
import os

import sys
sys.path.append(os.path.join(os.environ.get('HOME'), 'code'))
from CTFLib.config import get_settings

settings = get_settings()


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('dest', type=str, default='shell', nargs='?')


def handle(args: argparse.Namespace):
    get_shell(args.dest)


def get_shell(dest: str):
    cmd = f'musl-gcc -static {os.path.join(settings.BASE_PATH, "Commands/Pwn/shell.c")} -o {dest}'
    os.system(cmd)

