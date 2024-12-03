import sys

import click
from catalystwan.typed_list import DataSequence

sys.path.insert(0, "..")

from utils.session import create_session


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


def print_profile_details(profile_list):
    if profile_list is not None:
        for item in profile_list:
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Profile Name: {item.profile_name}")
            print(f"  - Id: {item.profile_id}")
            print(f"  - Solution: {item.solution}")
            print(f"  - Type: {item.profile_type}")
            print(f"  - Solution: {item.solution}")
            print(f"  - Created by: {item.created_by}")
            print(f"  - Last updated by: {item.last_updated_by}")
            print(f"  - Last updated on: {item.last_updated_on}")


# Get profiles
@click.command()
def get_profiles():
    system_profile_list = session.api.sdwan_feature_profiles.system.get_profiles()
    print_profile_details(system_profile_list)

    transport_profile_list = session.api.sdwan_feature_profiles.transport.get_profiles()
    print_profile_details(transport_profile_list)

    service_profile_list = session.api.sdwan_feature_profiles.service.get_profiles()
    print_profile_details(service_profile_list)


# Get config-groups
@click.command()
def get_groups():
    print("\n~~~ List of Configuration Groups\n")
    config_groups = session.api.config_group.get()
    for group in config_groups:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Config Group Name: {group.name}")
        print(f"- Description: {group.description}")
        print(f"- Solution: {group.solution}")

        profile_list = group.profiles
        if profile_list is not None:
            for profile in profile_list:
                print(f"- Profile Id: {profile.id}")
                print(f"  - Name: {profile.name}")
                print(f"  - Type: {profile.type}")
                print(f"  - Solution: {profile.solution}")
                print(f"  - Created by: {profile.created_by}")
                print(f"  - Last updated by: {profile.last_updated_by}")
                print(f"  - Last updated on: {profile.last_updated_on}")


if __name__ == "__main__":
    cli.add_command(get_groups)
    cli.add_command(get_profiles)

    with create_session() as session:
        cli()
