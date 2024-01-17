import re
import time
import subprocess

import sys

from distutils import command

# import os
import requests

# import yaml

import click

from pycelium.tools import soft
from pycelium.tools.cli.inventory import credentials, expand_network
from pycelium.tools.cli.config import (
    #config,
    #banner,
    RED,
    RESET,
    BLUE,
    PINK,
    YELLOW,
    GREEN,
)
from .main import *
from .config import *
from ..helpers import ConfigHelper


@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def setup(env):
    """subcommands for manage workspaces for cameraman"""
    # banner("User", env.__dict__)
    pass

def find_venv():
    for path in sys.path:
        # '/home/agp/Documents/cib/code/centesimal/iot/cameraman/venv/lib/python3.10/site-packages',
        m = re.match(r'(?P<virtualenv>.*/(venv|env|virtualenv))/lib/python[^/]+/(site-packages)$', path)
        if m:
            return m.groupdict()['virtualenv']
    
    
def configure_unit(unit_content, service_name, service_type='service', restart=True):
    # Write the service unit to a file
    fqservice = f"{service_name}.{service_type}"
    _tmp_file = f'/tmp/{fqservice}'
    unit_file_path = f'/etc/systemd/system/{fqservice}'
    with open(_tmp_file, 'w') as unit_file:
        unit_file.write(unit_content)
    subprocess.run(['sudo', 'mv', _tmp_file, unit_file_path])

    
    # Reload systemd to apply changes
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
    
    # Enable and start the service
    subprocess.run(['sudo', 'systemctl', 'enable', fqservice])
    if restart:
        subprocess.run(['sudo', 'systemctl', 'restart', fqservice])        
    

def _service(env, command):
    """List existing workspaces for cameraman"""

    # Specify the service name
    service_name = __file__.split('/')[-3]

    # user and group
    user = group = os.getlogin()
    home_dir = os.path.expanduser("~")
    # where is executable
    virtualenv = find_venv()

    if virtualenv is not None:
        exec_start =  f"{virtualenv}/bin/python {virtualenv}/bin/{service_name} {command}"
        environment =  f"Environment='PATH={virtualenv}/bin'"
    else:
        exec_start =  f"{home_dir}/.local/bin/{service_name} {command}"
        environment =  ""
                
    #cmd = f"/home/agp/Documents/cib/code/centesimal/iot/cameraman/venv/bin/cameraman {command}"

    # Define the service unit configuration
    service_unit= f"""
[Unit]
Description=Camera Supervisor Service
After=network.target

[Service]
ExecStart={exec_start}
{environment}

ProtectHome=false
WorkingDirectory={home_dir}/workspace/{service_name} 
#Restart=always
Restart=no
#RestartSec=5s
User={user}
Group={group}

[Install]
WantedBy=multi-user.target
"""
    
        
    timer_unit= f"""
[Unit]
Description=camera reset

[Timer]
Unit={service_name}.service
#OnCalendar=hourly
#OnCalendar=*:0/30
#OnCalendar=*:0/5

#OnBootSec=10min
#RandomizedDelaySec=15min
#OnActiveSec=15min
#OnCalendar=*-*-* 0/8:00:00
OnCalendar=*-*-* 00:00:00

[Install]
WantedBy=timers.target
"""
    
    configure_unit(service_unit, service_name, restart=False)
    configure_unit(timer_unit, service_name, service_type='timer')
    
    
    
@setup.command()
@click.option("--command", default="""inventory reset --network 192.168.2.1-256""")
@click.pass_obj
def service(env, command):
    """Install a reset service for all cameras in the network"""
    # force config loading
    config.callback()
    
    _service(env, command)


@setup.command()
@click.pass_obj
def autocomplete(env):
    """Create bash auto-completion script"""
    # force config loading
    config.callback()
    subprocess.run(['_CAMERAMAN_COMPLETE=bash_source cameraman > ~/.cameraman-complete.bash'], shell=True)
    print("for activation use:")
    print("source ~/.cameraman-complete.bash")
    
    
    
