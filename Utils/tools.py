import shutil
from pathlib import Path
from typing import Sequence, Any

from tqdm import trange, tqdm


def all_index(seq: Sequence, element: Any) -> list[int]:
    '''
    ### Important

    This function is only for finding element's index in sequence, not for
    subsequence.

    ---
    ### Example

    ```py
    index_list = all_index([1, 2, 3, 1, 2, 3, 1, 2, 3], 2)
    # index_list = [1, 4, 7]

    index_list = all_index('Hello World', 'C')
    # index_list = []

    index_list = all_index(b'BYTES', 69)
    # index_list = [3]
    ```
    '''

    if not element in seq:
        return []

    index_list = []
    offset = 0
    for _ in range(seq.count(element)):
        index = seq.index(element)
        index_list.append(offset + index)
        seq = seq[index + 1:]
        offset += index + 1
    return index_list


def check_command(cmd: str) -> bool:
    '''
    ### Example

    ```py
    if check_command('gcc'):
        # ...
    ```
    '''

    return shutil.which(cmd) is not None


def check_directory(directory: Path):
    '''
    ### Example

    ```py
    check_directory(Path('/tmp/test-dir'))
    ```
    '''

    directory.mkdir(parents=True, exist_ok=True)


def info(*args, **kwargs):
    print('[\033[94m*\033[0m]', *args, **kwargs)


def success(*args, **kwargs):
    print('[\033[92m+\033[0m]', *args, **kwargs)


def error(*args, **kwargs):
    print('[\033[91mX\033[0m]', *args, **kwargs)

