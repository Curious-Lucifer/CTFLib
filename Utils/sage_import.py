import sys

from ..settings import PLATFORM

if PLATFORM == 'darwin':
    sys.path.append('/private/var/tmp/sage-10.2-current/local/var/lib/sage/venv-python3.11.1/lib/python3.11/site-packages')

from sage.all import *

