import subprocess, re

from ..settings import BASE_PATH, PLATFORM
from ..Utils.sage_import import Matrix
from ..Utils.snippet import check_command, info, success


TOOLS_PATH = BASE_PATH / 'Tools'
SANDBOX_PATH = TOOLS_PATH / 'SandBox'

SANDBOX_PATH.mkdir(parents=True, exist_ok=True)


def fastcoll(prefix: bytes):
    if PLATFORM == 'darwin':
        raise NotImplementedError

    binary = TOOLS_PATH / 'fastcoll' / 'fastcoll'
    prefix_file = SANDBOX_PATH / 'fastcoll-prefix'
    msg1_file = SANDBOX_PATH /'fastcoll-msg1'
    msg2_file = SANDBOX_PATH /'fastcoll-msg2'

    if not binary.exists():
        if not check_command('g++'):
            raise FileNotFoundError('g++ command not found')

        info('Compiling fastcoll')
        try:
            subprocess.run(
                'g++ -O3 ./fastcoll/*.cpp -lboost_filesystem -lboost_program_options -lboost_system -static -o ./fastcoll/fastcoll',
                shell = True,
                check = True, 
                cwd = str(TOOLS_PATH), 
                stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE
            )
        except:
            raise FileNotFoundError("fastcoll compile failed")
        success('Compilation competed')

    prefix_file.write_bytes(prefix)

    info('Calculating md5 collision')
    try:
        subprocess.run(
            './fastcoll/fastcoll -p ./SandBox/fastcoll-prefix -o ./SandBox/fastcoll-msg1 ./SandBox/fastcoll-msg2', 
            shell = True, 
            check = True, 
            cwd = str(TOOLS_PATH), 
            stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE
        )
    except:
        raise FileNotFoundError("fastcoll execute error")
    success('Calculation completed')

    msg1, msg2 = msg1_file.read_bytes(), msg2_file.read_bytes()

    prefix_file.unlink()
    msg1_file.unlink()
    msg2_file.unlink()

    return msg1, msg2


def flatter(M):
    if PLATFORM == 'darwin':
        raise NotImplementedError

    if not check_command('flatter'):
        raise FileNotFoundError('flatter command not found')

    payload = '[[' + ']\n['.join(' '.join(map(str, row)) for row in M) + ']]'
    res = subprocess.check_output('flatter', input=payload.encode())
    return Matrix(M.nrows(), M.ncols(), map(int, re.findall(b'-?\\d+', res)))

