from io import BytesIO
import tarfile
import argparse


import docker


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('image', type=str)
    parser.add_argument('libc_path', type=str, nargs='?')


def handle(args: argparse.Namespace):
    get_libc(args.image, args.libc_path)


def get_libc(image: str, libc_path: str | None = None):
    libc_path = libc_path or ''

    client = docker.from_env()
    container = client.containers.create(image=image)
    stream, _ = container.get_archive('/lib/x86_64-linux-gnu/libc.so.6')

    fileobj = BytesIO()
    for s in stream:
        fileobj.write(s)

    fileobj.seek(0)
    with tarfile.open(fileobj=fileobj, mode='r') as tar:
        tar.extractall(path=libc_path)

    container.remove()

