# CTFLib

## Setup

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
