import re
import time

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
def inventory(env):
    """subcommands for manage workspaces for cameraman"""
    # banner("User", env.__dict__)
    pass

def _execute(env, network, command, retry=1, sleep=5):
    # force config loading
    config.callback()
    cfg = dict(env.__dict__)
    tool = ConfigHelper(env)
    
    def main():
        for pattern in network:
            for i, host in enumerate(expand_network(pattern)):            
                settings = tool.settings(host)
                auth = tool.auth(settings)
                url = tool.url(settings, "reset")
                for cmd in command:
                    method, cmd = tool.command(settings, cmd)
                    _url = url.format(**locals())
                    func = getattr(requests, method, requests.get)
                    try:
                        response = func(
                            _url,
                            auth=auth,
                            verify=False,
                            timeout=5, 
                        )
                    except requests.exceptions.ConnectionError:
                        print(f"{YELLOW}[{i}]: {host} not found{RESET}")
                        continue
                
                    # Check the response
                    if response.status_code == 200:
                        print(f"{GREEN}[{i}]: {host} OK{RESET}")
                    else:
                        print(f"{RED}[{i}]: {host} Error: {response.status_code} : {response}{RESET}")
    while retry:
        main()
        retry -= 1
        if retry:
            print(f"sleeping for {sleep} seconds")
            time.sleep(max(sleep, 0.5))
    

@inventory.command()
# @click.option("--network", default="192.168.22.[0-256]")
@click.option("--command", default=["reset"], multiple=True)
@click.option("--network", default=["192.168.6.200"], multiple=True)
@click.option("--retry", default=1)
@click.option("--sleep", default=3600*24)
@click.pass_obj
def execute(env, command, network, retry, sleep):
    """Create a new inventory for cameraman"""
    return _execute(env, network, command, retry, sleep)

@inventory.command()
# @click.option("--network", default="192.168.22.[0-256]")
@click.option("--network", default=["192.168.6.200"], multiple=True)
@click.option("--retry", default=1)
@click.option("--sleep", default=3600*24)
@click.pass_obj
def reset(env, network, retry, sleep):
    """Create a new inventory for cameraman"""
    return _execute(env, network, command=['reset'], retry=retry, sleep=sleep)

@inventory.command()
@click.pass_obj
def list(env):
    """List existing workspaces for cameraman"""
    # force config loading
    config.callback()

    # TODO: add your new workspace configuration folder here ...


    import systemd
    
    # Define the service unit configuration
    service_unit = f"""
    [Unit]
    Description=Your Python Service
    After=network.target
    
    [Service]
    ExecStart=/usr/bin/python3 /path/to/your/script.py
    WorkingDirectory=/path/to/your
    Restart=always
    User=nobody
    Group=nogroup
    
    [Install]
    WantedBy=multi-user.target
    """
    
    # Specify the service name
    service_name = 'your_service'
    
    # Create or update the service unit
    systemd.unit.write(service_name, service_unit)
    
    # Reload systemd to apply changes
    systemd.daemon.reload()
    
    # Enable and start the service
    systemd.unit.enable(service_name)
    systemd.unit.start(service_name)