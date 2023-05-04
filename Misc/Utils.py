import png


def write_png(png_list: list, output_file: str, alpha=False):
    """
    - input
        - `png_list (list)`
            - if `alpha` is `True`, then `[[(r, g, b, a), (r, g, b, a), ...], [], [], ...]`
            - if `alpha` is `False`, then `[[(r, g, b), (r, g, b), ...], [], [], ...]`
        - `output_file (str)`
        - `alpha (boolean)` : default is `False`
    """

    width = len(png_list[0])
    height = len(png_list)

    with open(output_file, 'wb') as f:
        w = png.Writer(width, height, greyscale=False, alpha=alpha)
        w.write(f, [sum(row, ()) for row in png_list])


def read_png(input_file: str):
    """
    - input : `input_file (str)`
    - output : `(png_list, alpha) (list, boolean)` , the `png_list` and `alpha`'s definition is same as `write_png`
    """

    r = png.Reader(filename=input_file)
    info = r.read()
    if info[3]['alpha']:
        png_list = [list(row) for row in list(info[2])]
        return [[(row[4 * i], row[4 * i + 1], row[4 * i + 2], row[4 * i + 3]) for i in range(len(row) // 4)] for row in png_list], True
    
    png_list = [list(row) for row in list(info[2])]
    return [[(row[3 * i], row[3 * i + 1], row[3 * i + 2]) for i in range(len(row) // 3)] for row in png_list], False


def all_index(seq: list, element):
    """
    - input : `seq (list)`, `element`
    - output : `index_list (list)`
    """

    index_list = []
    offset = 0
    for _ in range(seq.count(element)):
        index_list.append(offset + seq.index(element))
        seq = seq[seq.index(element) + 1:]
        offset = index_list[-1] + 1
    return index_list