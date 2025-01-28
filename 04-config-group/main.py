import click
from config_group import ConfigGroup
from service_profile import ServiceProfile
from system_profile import SystemProfile
from transport_profile import TransportProfile

from utils.session import create_session


@click.group()
def cli():
    """Command line tool for to manage Configuration Groups, Feature Profiles and Parcels"""
    pass


# --- Command: delete ---------------------------------------------------------
@click.command()
def delete():
    with create_session() as session:
        config_group = ConfigGroup(session)
        config_group.delete()


# --- Command: create ---------------------------------------------------------
@click.command()
def create():
    with create_session() as session:
        config_group = ConfigGroup(session)
        # config_group.delete()
        # config_group.create_profiles()
        config_group.create()
        config_group.print_summary()


# --- Run Commands ------------------------------------------------------------
cli.add_command(create)
cli.add_command(delete)

if __name__ == "__main__":
    cli()
