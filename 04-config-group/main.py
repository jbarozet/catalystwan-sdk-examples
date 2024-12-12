import click
from config_group import create_config_group, delete_config_group
from service_profile import create_service_profile, delete_service_profile
from system_profile import create_system_profile, delete_system_profile
from transport_profile import create_transport_profile, delete_transport_profile

from utils.session import create_session


@click.group()
def cli():
    """Command line tool for to manage Configuration Groups, Feature Profiles and Parcels"""
    pass


# --- Command: delete ---------------------------------------------------------
@click.command()
def delete():
    with create_session() as session:
        delete_config_group(session)
        delete_system_profile(session)
        delete_transport_profile(session)
        delete_service_profile(session)


# --- Command: Create ---------------------------------------------------------
@click.command()
def create():
    with create_session() as session:
        system_profile_id = create_system_profile(session)
        transport_profile_id = create_transport_profile(session)
        service_profile_id = create_service_profile(session)
        config_group_id = create_config_group(session, system_profile_id, transport_profile_id, service_profile_id)

        print("\n- Summary")
        print("  - ConfigGroup ID:", config_group_id)
        print("  - System Profile ID:", system_profile_id)
        print("  - Transport Profile ID:", transport_profile_id)
        print("  - Service Profile ID:", service_profile_id)


# --- Run Commands ------------------------------------------------------------
cli.add_command(create)
cli.add_command(delete)

if __name__ == "__main__":
    cli()
    cli()
    cli()
    cli()
    cli()
    cli()
