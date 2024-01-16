"""CLI for 'Cameraman' package.

# Autocompletion

https://click.palletsprojects.com/en/8.1.x/shell-completion/

_CAMERAMAN_COMPLETE=IGNORE_WINGDEBUG=0 bash_source cameraman > ~/.cameraman-complete.bash

. ~/.cameraman-complete.bash

"""
import sys
import os
if os.environ.get('IGNORE_WINGDEBUG', True):
    try:
        # print(f"Trying to connect to a remote debugger..")
        sys.path.append(os.path.dirname(__file__))
        from . import wingdbstub
    except Exception:
        print("Remote debugging is not found or configured...")
else:
    print("Remote debugging is not selected")
    

# -----------------------------------------------
# import main cli interface (root)
# -----------------------------------------------

from .main import *
from .config import *
from .workspace import *

# -----------------------------------------------
# import other project submodules/subcommands
# -----------------------------------------------

from .inventory import inventory
from .setup import setup
# from .plan import plan
# from .real import real
# from .roles import role
# from .run import run
# from .target import target
# from .test import test
# from .users import user
# from .watch import watch

