# CTFLib

## Requirement
### Mac

1. Install Python 3.11
2. Install `pwntools`
    ```shell
    brew install cmake pkg-config
    git clone https://github.com/unicorn-engine/unicorn.git
    cd unicorn/bindings/python
    sudo make install
    cd ../../..
    sudo rm -rf unicorn
    sudo pip3 install pwntools
    ```
3. Install [SageMath](https://github.com/3-manifolds/Sage_macOS/releases)
4. Install other requirements
    ```shell
    pip3 install -r requirements.txt
    brew install tmux
    ```
5. Install [flatter](https://github.com/keeganryan/flatter)
    ```shell
    
    ```


### Ubuntu

1. Install requirements
    ```shell
    sudo apt install sagemath tmux libboost-filesystem-dev libboost-program-options-dev libgmp-dev
    sudo pip3 install pwntools
    cd $HOME/code/CTFLib
    pip3 install -r requirements.txt
    ```
2. Install [flatter](https://github.com/keeganryan/flatter)
    ```shell
    sudo apt install libgmp-dev libmpfr-dev fplll-tools libfplll-dev libeigen3-dev
    git clone https://github.com/keeganryan/flatter.git && cd flatter
    mkdir build && cd ./build
    cmake ..
    make
    sudo make install
    sudo ldconfig
    cd ../.. && rm -rf flatter
    ```


---
## Usage
```python
import sys, os

sys.path.append(os.path.join(os.environ.get('HOME'), 'code'))

from CTFLib.all import *
```

