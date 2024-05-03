# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Configuration
# Config Groups, Feature Profiles, Policy Groups
#
# Description:
#
#
# =========================================================================

import os
from datetime import datetime

import click

from manager import MyManager
from utils import Workdir


def help():
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=10.10.1.1")
    print("set vmanage_port=8443")
    print("set vmanage_user=admin")
    print("set vmanage_password=admin")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=10.10.1.1")
    print("export vmanage_port=8443")
    print("export vmanage_user=admin")
    print("export vmanage_password=admin")


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def backup():
    """
    Save config-groups and feature profiles
    Save devices associated with config-group
    Save deployment values
    Backup data hierarchy:
        config_groups
            associated
            groups
            values
        feature_profiles
            cli
            system
            transport
            service
            policy-object
    """

    manager.save_groups()
    manager.save_associated_devices()
    manager.save_config_group_values()
    manager.save_sdwan_profiles()
    manager.save_sdrouting_profiles()


@click.command()
def profiles_summary():
    dir = "data/outputs/"

    manager = MyManager(url, user, password, dir)
    if not manager.status:
        exit(1)

    manager.list_sdwan_profiles_summary()
    manager.list_sdrouting_profiles_summary()


@click.command()
def profiles_categories():
    dir = "data/outputs/"

    manager = MyManager(url, user, password, dir)
    if not manager.status:
        exit(1)

    manager.list_profiles_categories()


# Add commands to CLI
cli.add_command(profiles_summary)
cli.add_command(profiles_categories)
cli.add_command(backup)

# Main
if __name__ == "__main__":

    url = os.environ.get("vmanage_host")
    user = os.environ.get("vmanage_user")
    password = os.environ.get("vmanage_password")
    dir = "data/outputs/"

    if url is None or user is None or password is None:
        help()
        exit()

    # Create backup folder
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    dir = "data/" + current_datetime
    workdir = Workdir(dir)

    # Create SD-WAN Manager session
    manager = MyManager(url, user, password, workdir)
    if not manager.status:
        exit(1)

    cli()
