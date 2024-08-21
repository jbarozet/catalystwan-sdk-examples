# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Device Config
# Using Config Group and Feature Profiles
#
# =========================================================================

import sys

import click

sys.path.insert(0, "..")
from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.models.configuration.feature_profile.sdwan.system.aaa import AAAParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.bfd import BFDParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.omp import OMPParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import TransportVpnParcel

from utils.session import create_session

# from catalystwan.models.configuration.feature_profile.sdwan.system.aaa import AAAParcel


def print_profile_details(api):
    profile_list = api.get_profiles()
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


# Get profiles - Not yet available. Syntax may change.
@click.command()
def get_profiles():
    print("\n~~~ List of Features Profiles\n")

    # system_api = session.api.sdwan_feature_profiles.system

    profile_list = session.api.sdwan_feature_profiles.system.get_profiles()
    print(profile_list)
    if profile_list is not None:
        for profile in profile_list:
            print(f"\n~~~ Profile ID: {profile.profile_id}")
            print(f"  - name: {profile.profile_name}")
            print(f"  - solution: {profile.solution}")
            print(f"  - type: {profile.profile_type}")
            print(f"  - last updated: {profile.last_updated_on} by {profile.last_updated_by}")

    parcel_list = session.api.sdwan_feature_profiles.system.get_parcels("80779dbb-174d-4039-a054-467fe2e897bc", BFDParcel)
    print(parcel_list)
    if parcel_list is not None:
        for parcel in parcel_list:
            print("~~~ System Parcel")
            print(f"  - id: {parcel.parcel_id}")
            print(f"  - type: {parcel.parcel_type}")
            print(f"  - name: {parcel.payload.parcel_name}")
            print(f"  - description: {parcel.payload.parcel_description}")
            parcel.payload.model_dump_json(by_alias=True, indent=4)

    # parcel_list = session.api.sdwan_feature_profiles.transport.get_parcels("59f09d1b-07d4-4597-960c-2760fb199c17", TransportVpnParcel)
    # print(parcel_list)

    # parcel_list = session.api.sdwan_feature_profiles.system.get_parcels("80779dbb-174d-4039-a054-467fe2e897bc", OMPParcel)
    # print(parcel_list)

    # print_profile_details(system_api)

    # transport_api = session.api.sdwan_feature_profiles.transport
    # print_profile_details(transport_api)

    # service_api = session.api.sdwan_feature_profiles.service
    # print_profile_details(service_api)

    # cli_api = session.api.sdwan_feature_profiles.cli
    # print_profile_details(cli_api)

    # policy_api = session.api.sdwan_feature_profiles.policy_object
    # print_profile_details(policy_api)

    # system_api = session.api.sd_routing_feature_profiles.system
    # print_profile_details(system_api)

    # cli_api = session.api.sd_routing_feature_profiles.cli
    # print_profile_details(cli_api)

    session.close()


cli.add_command(get_groups)
cli.add_command(get_profiles)

# Create vManage session
session = create_session()

if __name__ == "__main__":
    cli()
