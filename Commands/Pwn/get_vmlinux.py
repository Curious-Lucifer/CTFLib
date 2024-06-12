import argparse
import os

from CTFLib.config import get_settings

settings = get_settings()


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('bzImage_dest', type=str, default='bzImage', nargs='?')
    parser.add_argument('vmlinux_dest', type=str, default='vmlinux', nargs='?')


def handle(args: argparse.Namespace):
    get_vmlinux(args.bzImage_dest, args.vmlinux_dest)


def get_vmlinux(bzImage_dest: str, vmlinux_dest: str):
    cmd = f'{os.path.join(settings.BASE_PATH, "Commands/Pwn/extract-vmlinux")} {bzImage_dest} > {vmlinux_dest}'
    os.system(cmd)

