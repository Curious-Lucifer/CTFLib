# CTFLib

## Requirement
```bash
sudo apt install sagemath tmux libboost-filesystem-dev libboost-program-options-dev
sudo pip3 install pwntools z3-solver
pip3 install pycryptodome gmpy2 tqdm requests pypng beautifulsoup4
```

[flatter](https://github.com/keeganryan/flatter) : 
```bash
git clone https://github.com/keeganryan/flatter.git && cd flatter
sudo apt install libgmp-dev libmpfr-dev fplll-tools libfplll-dev libeigen3-dev
mkdir build && cd ./build
cmake ..
make
sudo make install
sudo ldconfig
cd ../.. && rm -rf flatter
```

## Usage
```python
import sys
sys.path.append("<CTFLib parent directory's path>")

from CTFLib.all import *
```

## Functionality
- `Crypto`
  - `Block_Cipher`
    - `padding_oracle_attack`
    - `GCM_Forbidden_Attack`
      - `append`
      - `calc_H`
      - `calc_EJ0`
      - `calc_auth_tag`
  - `Classical_Cipher`
    - `simple_freq_analysis`
  - `Hash`
    - `length_extension_attack`
  - `PRNG`
    - `lcg_attack`
    - `MT19937_rand2state`
    - `MT19937_state2rand`
    - `MT19937_gen_next_state`
    - `MT19937_attack`
  - `RSA`
    - `pem2key`
    - `factor_online`
    - `factor_n_with_d`
    - `fermat_factor`
    - `pollard_algorithm`
    - `william_algorithm`
    - `wiener_attack`
    - `LSB_oracle_attack`
    - `bleichenbacher_1998`
    - `stereotyped_message`
    - `known_high_bits_of_p`
    - `franklin_reiter`
    - `coppersmith_short_pad_attack`
  - `Utils`
    - `xor`
    - `egcd`
    - `crt`
    - `generate_lcg`
    - `legendre_symbol`
    - `ceil_int`
    - `floor_int`
    - `polynomialgcd`
    - `un_bitshift_right_xor`
    - `un_bitshift_left_xor_mask`
- `Misc`
  - `Utils`
    - `write_png`
    - `read_png`
    - `all_index`