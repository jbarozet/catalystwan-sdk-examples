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

from manager import ConfigGroupTable, MyManager, SDRoutingProfileTable, SDWANProfileTable
from utils import Workdir


def help():
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=10.10.1.1")
    print("set vmanage_port=8443")
    print("set vmanage_user=admin")
    print("set vmanage_password=some_password")
    print("")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=10.10.1.1")
    print("export vmanage_port=8443")
    print("export vmanage_user=admin")
    print("export vmanage_password=some_password")


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

    # Create backup folder
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    dir = "data/" + current_datetime
    workdir = Workdir(dir)

    config_group_table = ConfigGroupTable(manager)
    config_group_table.save_groups(workdir)
    sdwan_profiles_table = SDWANProfileTable(manager)
    sdwan_profiles_table.save_profiles(workdir)
    sdrouting_profiles_table = SDRoutingProfileTable(manager)
    sdrouting_profiles_table.save_profiles(workdir)


@click.command()
def list_groups():
    config_group_table = ConfigGroupTable(manager)
    config_group_table.list_groups()


@click.command()
def list_profiles():
    profiles_table = SDWANProfileTable(manager)
    profiles_table.list()


@click.command()
def list_profile_categories():
    profile_table = SDWANProfileTable(manager)
    profile_table.list_categories()


# Add commands to CLI
cli.add_command(backup)
cli.add_command(list_groups)
cli.add_command(list_profiles)
cli.add_command(list_profile_categories)


# Main
if __name__ == "__main__":

    url = os.environ.get("vmanage_host")
    user = os.environ.get("vmanage_user")
    password = os.environ.get("vmanage_password")
    dir = "data/outputs/"

    if url is None or user is None or password is None:
        help()
        exit()

    # Create SD-WAN Manager session
    manager = MyManager(url, user, password)
    if not manager.status:
        exit(1)

    cli()
