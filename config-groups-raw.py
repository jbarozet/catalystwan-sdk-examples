# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Device Config
# Using Config Group and Feature Profiles
#
# Description:
#   Get config-groups and feature profiles
#   Get devices associated with config-group
#   Get deployment values
#
# Output data hierarchy:
#   config_groups
#       associated
#       groups
#       values
#
#   feature_profiles
#       cli
#       system
#       transport
#       service
#       policy-object
#
# =========================================================================

import os

import click

from manager import MyManager


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
def save_groups():
    manager.save_groups()
    manager.save_associated_devices()
    manager.save_config_group_values()


@click.command()
def save_profiles():
    manager.save_profiles


@click.command()
def profiles_summary():
    manager.list_sdwan_profiles_summary()
    manager.list_sdrouting_profiles_summary()


@click.command()
def profiles_categories():
    manager.list_profiles_categories()


@click.command()
def save_associated_devices():
    manager.save_associated_devices()


# Add commands to CLI
cli.add_command(save_groups)
cli.add_command(save_profiles)
cli.add_command(profiles_summary)
cli.add_command(profiles_categories)
cli.add_command(save_associated_devices)

# Main
if __name__ == "__main__":

    url = os.environ.get("vmanage_host")
    user = os.environ.get("vmanage_user")
    password = os.environ.get("vmanage_password")

    if url is None or user is None or password is None:
        help()
        exit()

    manager = MyManager(url, user, password)

    if not manager.status:
        exit(1)

    manager.create_workdir()

    cli()
