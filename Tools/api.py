from pathlib import Path
import subprocess
import tempfile
import re

from ..config import get_settings
from ..Utils.tools import check_command, check_directory, info, success


settings = get_settings()


def fastcoll(prefix: bytes) -> tuple[bytes, bytes]:
    '''
    ### Example

    ```py
    payload0, payload1 = fastcoll(b'12345678')
    # payload0.startswith(b'12345678')
    # payload1.startswith(b'12345678')
    # payload0 != payload1
    # hashlib.md5(payload0) == hashlib.md5(payload1)
    ```
    '''

    if settings.PLATFORM == 'darwin':
        raise NotImplementedError

    binary = settings.TOOLS_PATH / 'fastcoll' / 'fastcoll'
    if not binary.exists():
        if not check_command('g++'):
            raise FileNotFoundError('g++ command not found')

        info('Compiling fastcoll...')
        subprocess.run(
            'g++ -O3 ./fastcoll/*.cpp -lboost_filesystem -lboost_program_options -lboost_system -static -o ./fastcoll/fastcoll', 
            shell = True, 
            check = True, 
            cwd = settings.TOOLS_PATH, 
            stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE
        )
        success('Compilation finished successfully')

    check_directory(settings.SANDBOX_PATH)
    with tempfile.TemporaryDirectory(dir=settings.SANDBOX_PATH) as temp_dir:
        temp_path = Path(temp_dir)
        prefix_path = temp_path / 'prefix'
        payload0_path = temp_path / 'payload0'
        payload1_path = temp_path / 'payload1'

        prefix_path.write_bytes(prefix)

        info('Calculating md5 collision...')
        subprocess.run(
            [binary, '-p', prefix_path, '-o', payload0_path, payload1_path], 
            check = True, 
            stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE
        )
        success('Calculation finished successfully')

        payload0, payload1 = payload0_path.read_bytes(), payload1_path.read_bytes()

    return payload0, payload1


def flatter(Matrix: list[list[int]]):
    '''
    ### Example

    ```py

    ```
    '''

    if settings.PLATFORM == 'darwin':
        raise NotImplementedError

    if not check_command('flatter'):
        raise FileNotFoundError('flatter command not found')

    size = len(Matrix)
    payload = '[[' + ']\n['.join(' '.join(map(str, row)) for row in Matrix) + ']]'

    info('Reducing lattice...')
    result = subprocess.check_output('flatter', input=payload.encode())
    success('Lattice reduction finished successfully')

    result = [int(num) for num in  re.findall(b'-?\\d+', result)]
    return [[result[i + j * size] for i in range(size)] for j in range(size)]

