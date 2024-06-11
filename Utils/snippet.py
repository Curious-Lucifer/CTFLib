
def local(binary: str | list[str], libc: str | None = None, env: dict[str, str] | None = None):
    '''
    ### Example

    ```py
    r = local('./binary')

    # or

    r = local('./binary', './libc.so.6')
    ```
    '''

    from pwn import process

    env = env or {}
    if libc:
        env['LD_PRELOAD'] = libc
    return process(binary, env=env)


def nc(cmd: str):
    '''
    ### Example

    ```py
    r = nc('nc 127.0.0.1 20000')

    # or

    r = nc('127.0.0.1 20000')
    ```
    '''

    from pwn import remote

    server, port = cmd.removeprefix('nc ').split()
    return remote(server, int(port))

