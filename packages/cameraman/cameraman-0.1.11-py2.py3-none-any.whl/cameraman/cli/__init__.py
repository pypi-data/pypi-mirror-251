"""CLI for 'Cameraman' package.

# Autocompletion

https://click.palletsprojects.com/en/8.1.x/shell-completion/

_CAMERAMAN_COMPLETE=bash_source cameraman > ~/.cameraman-complete.bash
. ~/.cameraman-complete.bash



Debug Example:

export WINGHOME=True
export WINGDB_HOSTPORT=10.220.2.200:50005

"""
import sys
import os
ACTIVE_WINGDEBUG = os.environ.get('ACTIVE_WINGDEBUG', 'False').lower()
    
if ACTIVE_WINGDEBUG in ('true', 'yes', '1'):
    try:
        # print(f"Trying to connect to a remote debugger..")
        sys.path.append(os.path.dirname(__file__))
        from . import wingdbstub
    except Exception:
        print("Remote debugging is not found or configured: Use ACTIVE_WINGDEBUG=True to activate")
else:
    #print("Remote debugging is not selected") # don't show: problem with bash_source autocompletion
    pass
    

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

