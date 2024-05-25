
def pixel_matrix_to_png(
    pixel_matrix: list[list[tuple[int, int, int, int] | tuple[int, int, int]]], 
    output_file: str
):
    '''
    ### Example
    
    ```py
    # 0 ≤ r, g, b, a < 256
    pixel_matrix = [
        [(r, g, b, a), (r, g, b, a), ...], 
        [(r, g, b, a), (r, g, b, a), ...], 
        ...
        [(r, g, b, a), (r, g, b, a), ...]
    ]

    # or

    # 0 ≤ r, g, b < 256
    pixel_matrix = [
        [(r, g, b), (r, g, b), ...], 
        [(r, g, b), (r, g, b), ...], 
        ...
        [(r, g, b), (r, g, b), ...]
    ]

    pixel_matrix_to_png(pixel_matrix, 'output.png')
    ```
    '''

    import png

    height, width = len(pixel_matrix), len(pixel_matrix[0])
    alpha = (len(pixel_matrix[0][0]) == 4)

    w = png.Writer(width, height, greyscale=False, alpha=alpha)
    with open(output_file, 'wb') as f:
        w.write(f, [sum(row, ()) for row in pixel_matrix])


def png_to_pixel_matrix(
    input_file: str
) -> tuple[list[list[tuple[int, int, int, int] | tuple[int, int, int]]], bool]:
    '''
    ### Example
    
    ```py
    pixel_matrix, alpha = png_to_pixel_matrix('input.png')
    ```
    '''

    import png

    r = png.Reader(filename=input_file)
    png_data = r.read()

    if png_data[3]['alpha']:
        pixel_matrix = [
            [tuple(row[i: i + 4]) for i in range(0, len(row), 4)]
            for row in list(png_data[2])
        ]
    else:
        pixel_matrix = [
            [tuple(row[i: i + 3]) for i in range(0, len(row), 3)]
            for row in list(png_data[2])
        ]

    return pixel_matrix, png_data[3]['alpha']


