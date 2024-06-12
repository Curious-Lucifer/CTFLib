from PIL import Image

class PNGConverter:
    @staticmethod
    def list2png(
        pixel_list: list[tuple[int, int, int, int] | tuple[int, int, int]], 
        width: int, height: int, 
        output_path: str
    ):
        '''
        ### Example

        ```py
        # 0 ≤ r, g, b, a < 256
        PNGConverter.list2png(
            [(r, g, b, a), (r, g, b, a), ...], 
            width, height, 
            'output.png'
        )

        # or

        # 0 ≤ r, g, b < 256
        PNGConverter.list2png(
            [(r, g, b), (r, g, b), ...], 
            width, height, 
            'output.png'
        )
        ```
        '''

        mode = 'RGBA' if len(pixel_list[0]) == 4 else 'RGB'
        image = Image.new(mode, (width, height))
        image.putdata(pixel_list)
        image.save(output_path)

    @staticmethod
    def matrix2png(
        pixel_matrix: list[list[tuple[int, int, int, int] | tuple[int, int, int]]], 
        output_path: str
    ):
        '''
        ### Example

        ```py
        # 0 ≤ r, g, b, a < 256
        matrix = [
            [(r, g, b, a), (r, g, b, a), ...], 
            [(r, g, b, a), (r, g, b, a), ...], 
            ...
            [(r, g, b, a), (r, g, b, a), ...]
        ]

        # or

        # 0 ≤ r, g, b < 256
        matrix = [
            [(r, g, b), (r, g, b), ...], 
            [(r, g, b), (r, g, b), ...], 
            ...
            [(r, g, b), (r, g, b), ...]
        ]

        PNGConverter.matrix2png(matrix, 'output.png')
        ```
        '''

        pixel_list, width, height = PNGConverter.matrix2list(pixel_matrix)
        PNGConverter.list2png(pixel_list, width, height, output_path)

    @staticmethod
    def png2list(png_path: str):
        '''
        ### Example

        ```py

        ```
        '''

        image = Image.open(png_path)
        width, height = image.size
        return list(image.getdata()), width, height

    @staticmethod
    def png2matrix(png_path: str):
        '''
        ### Example

        ```py

        ```
        '''

        pixel_list, width, height = PNGConverter.png2list(png_path)
        return PNGConverter.list2matrix(pixel_list, width, height)

    @staticmethod
    def list2matrix(
        pixel_list: list[tuple[int, int, int, int] | tuple[int, int, int]], 
        width: int, height: int
    ):
        '''
        ### Example

        ```py

        ```
        '''

        if len(pixel_list) != width * height:
            raise ValueError('`pixel_list`\'s length must equal to `width` * `height`')

        pixel_matrix = [
            pixel_list[width * i: width * (i + 1)] for i in range(height)
        ]
        return pixel_matrix

    @staticmethod
    def matrix2list(
        pixel_matrix: list[list[tuple[int, int, int, int] | tuple[int, int, int]]]
    ):
        '''
        ### Example

        ```py

        ```
        '''

        width = len(pixel_matrix[0])
        height = len(pixel_matrix)
        return sum(pixel_matrix, []), width, height

