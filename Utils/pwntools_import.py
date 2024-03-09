from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

