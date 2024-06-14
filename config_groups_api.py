# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Device Config
# Using Config Group and Feature Profiles
#
# =========================================================================

import click

from session import create_session

# from catalystwan.models.configuration.feature_profile.sdwan.system.aaa import AAAParcel


def print_profile_details(api):
    profiles = api.get_profiles()
    for item in profiles:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Profile Name: {item.profile_name}")
        print(f"  - Id: {item.profile_id}")
        print(f"  - Solution: {item.solution}")
        print(f"  - Type: {item.profile_type}")
        print(f"  - Solution: {item.solution}")
        print(f"  - Created by: {item.created_by}")
        print(f"  - Last updated by: {item.last_updated_by}")
        print(f"  - Last updated on: {item.last_updated_on}")
        # parcels = api.get_parcels(profile_id=item.profile_id, parcel_type=AAAParcel)
        # for item in parcels:
        #     payload = item.model_dump_json()
        #     print(payload)


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


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

    session.close()


# Get profiles.
# Filtering available with:
#   profile = system_api.get_profiles().filter(profile_name="JMB_SDWAN_Basic").single_or_default()
@click.command()
def get_profiles():
    print("\n~~~ List of Features Profiles\n")

    system_api = session.api.sdwan_feature_profiles.system
    print_profile_details(system_api)

    transport_api = session.api.sdwan_feature_profiles.transport
    print_profile_details(transport_api)

    service_api = session.api.sdwan_feature_profiles.service
    print_profile_details(service_api)

    # Not implemented yet -catalystwan 0.33.7.dev6
    cli_api = session.api.sdwan_feature_profiles.cli
    print_profile_details(cli_api)

    # Not implemented yet
    # policy_api = session.api.sdwan_feature_profiles.policy_object
    # print_profile_details(policy_api)

    # Not implemented yet
    # system_api = session.api.sd_routing_feature_profiles.system
    # print_profile_details(system_api)

    # Not implemented yet
    # cli_api = session.api.sd_routing_feature_profiles.cli
    # print_profile_details(cli_api)

    session.close()


cli.add_command(get_groups)
cli.add_command(get_profiles)

# Create vManage session
session = create_session()

if __name__ == "__main__":
    cli()
