from pwn import remote, process, context


def local(binary: str | list[str], libc: str | None = None, env: dict[str, str] | None = None, verbose: bool = True):
    '''
    ### Example

    ```py
    r = local('./binary')

    # or

    r = local('./binary', './libc.so.6')
    ```
    '''

    if verbose:
        context.log_level = 20
    else:
        context.log_level = 'error'

    env = env or {}
    if libc:
        env['LD_PRELOAD'] = libc
    return process(binary, env=env)


def nc(cmd: str, verbose: bool = True):
    '''
    ### Example

    ```py
    r = nc('nc 127.0.0.1 20000')

    # or

    r = nc('127.0.0.1 20000')
    ```
    '''

    if verbose:
        context.log_level = 20
    else:
        context.log_level = 'error'

    server, port = cmd.removeprefix('nc ').split()
    return remote(server, int(port))

