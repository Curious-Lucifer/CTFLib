# CTFLib

## Requirement

- Docker

---
## Setup For Ubuntu
> 需要把 `CTFLib` 所在的資料夾加到 `PYTHONPATH` 中

如果只使用 `CTFLib.Utils` 和 `CTFLib.Pwn`

```shell
./setup.sh min
```

如果有使用到 `CTFLib.Misc`

```shell
./setup.sh misc
```

如果有使用到 `CTFLib.Tools`

```shell
./setup.sh tools
```

如果有使用到 `CTFLib.Crypto`

```shell
./setup.sh crypto
```

如果整個 `CTFLib` 都有被使用到

```shell
./setup.sh all
```


---
## Usage

Pwn : 

```py
from pwn import *

import sys, os
sys.path.append(os.path.join(os.environ.get('HOME'), 'code'))
from CTFLib.Utils import *
from CTFLib.Pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.delete_corefiles = True


```


Utils : 

```py
from pwn import *

import sys, os
sys.path.append(os.path.join(os.environ.get('HOME'), 'code'))
from CTFLib.Utils import *


```


---
## Setup For Mac
> 未完成

### SageMath

把類似 `/Applications/SageMath-10-2.app/Contents/Frameworks/Sage.framework/Versions/10.2/local/var/lib/sage/venv-python3.11.1/lib/python3.11/site-packages` 的 Path 加到 `PYTHONPATH` 中



