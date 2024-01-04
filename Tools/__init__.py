import os, subprocess, sys

if sys.platform == 'darwin':
    BASE_DIR = '/Users/curious/code/CTFLib/Tools/'
else:
    BASE_DIR = '/home/curious/code/CTFLib/Tools/'
SANDBOX_DIR = os.path.join(BASE_DIR, 'SandBox/')

if not os.path.exists(SANDBOX_DIR):
    os.makedirs(SANDBOX_DIR)


def check_command(command: str):
    """
    - input : `command (str)`
    - output : `check (bool)`
    """

    try:
        res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return res.returncode == 0
    except:
        return False


def fastcoll(prefix: bytes):
    """
    - input : `prefix (bytes)`
    - output : `msg1 (bytes)`, `msg2 (bytes)`
    """

    if not os.path.isfile(os.path.join(BASE_DIR, 'fastcoll/fastcoll')):
        if not check_command('g++ --version'):
            raise FileNotFoundError("fastcoll compile failed")

        print('[\033[1m\033[92m+\033[0m\033[0m] Compiling fastcoll')
        try:
            subprocess.run(
                'g++ -O3 ./fastcoll/*.cpp -lboost_filesystem -lboost_program_options -lboost_system -static -o ./fastcoll/fastcoll',
                shell = True,
                check = True, 
                cwd = BASE_DIR, 
                stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE
            )
        except:
            raise FileNotFoundError("fastcoll compile failed")
        print('[\033[94m*\033[0m] Compilation completed')

    open(os.path.join(SANDBOX_DIR, 'fastcoll-prefix'), 'wb').write(prefix)

    print('[\033[1m\033[92m+\033[0m\033[0m] Calculating md5 collision')
    try:
        subprocess.run(
            './fastcoll/fastcoll -p ./SandBox/fastcoll-prefix -o ./SandBox/fastcoll-msg1 ./SandBox/fastcoll-msg2', 
            shell = True, 
            check = True, 
            cwd = BASE_DIR, 
            stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE
        )
    except:
        raise FileNotFoundError("fastcoll execute error")
    print('[\033[94m*\033[0m] Calculation completed')

    msg1 = open(os.path.join(SANDBOX_DIR, 'fastcoll-msg1'), 'rb').read()
    msg2 = open(os.path.join(SANDBOX_DIR, 'fastcoll-msg2'), 'rb').read()

    os.remove(os.path.join(SANDBOX_DIR, 'fastcoll-prefix'))
    os.remove(os.path.join(SANDBOX_DIR, 'fastcoll-msg1'))
    os.remove(os.path.join(SANDBOX_DIR, 'fastcoll-msg2'))

    return msg1, msg2

