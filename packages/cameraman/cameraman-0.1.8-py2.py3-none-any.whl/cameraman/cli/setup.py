import re
import time
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
    

@setup.command()
@click.option("--command", default="inventory execute --command reset")
@click.pass_obj
def service(env, command):
    """List existing workspaces for cameraman"""
    # force config loading
    config.callback()

    #import systemd_service as systemd
    import subprocess

    # Specify the service name
    service_name = __file__.split('/')[-3]

    # user and group
    user = group = os.getlogin()
    home_dir = os.path.expanduser("~")
    # where is executable
    virtualenv = find_venv()

    if virtualenv is not None:
        exec_start =  f"{virtualenv}/bin/python {virtualenv}/bin/{service_name} {command}"
        environment =  "Environment='PATH={virtualenv}/bin'"
    else:
        exec_start =  f"{home_dir}/.local/bin/{service_name} {command}"
        environment =  ""
                
    #cmd = f"/home/agp/Documents/cib/code/centesimal/iot/cameraman/venv/bin/cameraman {command}"

    # Define the service unit configuration
    service_unit = f"""
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
RestartSec=5s
User={user}
Group={group}

[Install]
WantedBy=multi-user.target
"""
    
    
    # Create or update the service unit

    
    # Write the service unit to a file
    _tmp_file = f'/tmp/{service_name}.service'
    unit_file_path = f'/etc/systemd/system/{service_name}.service'
    with open(_tmp_file, 'w') as unit_file:
        unit_file.write(service_unit)
    subprocess.run(['sudo', 'mv', _tmp_file, unit_file_path])

        
    
    # Reload systemd to apply changes
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
    
    # Enable and start the service
    subprocess.run(['sudo', 'systemctl', 'enable', service_name])
    subprocess.run(['sudo', 'systemctl', 'start', service_name])    
    
    
    ## Reload systemd to apply changes
    #systemd.daemon.reload()
    
    ## Enable and start the service
    #systemd.unit.enable(service_name)
    #systemd.unit.start(service_name)