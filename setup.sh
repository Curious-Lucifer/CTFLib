#!/bin/bash -e


if [[ $# == 0 ]]; then
    echo "Usage : "
    echo "Minimum setup : ./setup min"
    echo "Misc setup    : ./setup misc"
    echo "Tools setup   : ./setup tools"
    echo "Crypto setup  : ./setup crypto"
    echo "Command setup : ./setup cmd"
    echo "All setup     : ./setup all"
    exit 0
fi


minimun_setup() {
    # Utils
    sudo pip3 install pwntools tqdm
}


misc_setup() {
    # Misc
    pip3 install pypng
}


tools_setup() {
    # Tools

    ## fastcoll
    sudo apt install g++ libboost-filesystem-dev libboost-program-options-dev libgmp-dev

    ## flatter
    sudo apt install sagemath tmux libboost-filesystem-dev libboost-program-options-dev libgmp-dev
    git clone https://github.com/keeganryan/flatter.git
    mkdir -p flatter/build
    cd flatter/build
    cmake ..
    make
    sudo make install
    sudo ldconfig
    cd ../..
    rm -rf flatter
}


crypto_setup() {
    pip3 install pycryptodome
    sudo apt install sagemath
}


command_setup() {
    sudo apt install musl-tools
    pip3 install docker

    if [ -n "$ZSH_VERSION" ]; then
        echo 'alias ctf=$HOME/code/CTFLib/ctf.py' >> ~/.zshrc
        source ~/.zshrc
    else
        echo 'alias ctf=$HOME/code/CTFLib/ctf.py' >> ~/.bashrc
        source ~/.bashrc
    fi
}


if [[ $1 == "min" ]]; then
    minimun_setup
elif [[ $1 == "misc" ]]; then
    minimun_setup
    misc_setup
elif [[ $1 == "tools" ]]; then
    minimun_setup
    tools_setup
elif [[ $1 == "crypto" ]]; then
    minimun_setup
    misc_setup
    tools_setup
    crypto_setup
elif [[ $1 == "cmd " ]]; then
    command_setup
elif [[ $1 == "all" ]]; then
    minimun_setup
    misc_setup
    tools_setup
    command_setup
    crypto_setup
fi
