# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Device Config
# Using Config Group and Feature Profiles
#
# =========================================================================

import sys
from uuid import UUID

import click

sys.path.insert(0, "..")
from catalystwan.models.configuration.feature_profile.sdwan.system.aaa import AAAParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.basic import BasicParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.bfd import BFDParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.global_parcel import GlobalParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.logging_parcel import LoggingParcel
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


def print_parcel_details(parcel_list):
    for parcel in parcel_list:
        print(f"** Parcel: {parcel.parcel_type}")
        print(f"  - id: {parcel.parcel_id}")
        print(f"  - type: {parcel.parcel_type}")
        print(f"  - name: {parcel.payload.parcel_name}")
        print(f"  - description: {parcel.payload.parcel_description}")
        print(f"  - Payload: {parcel.payload.model_dump_json(by_alias=True, indent=4)}")


def print_system_parcel_details(profile_id: UUID):
    parcel_list = session.api.sdwan_feature_profiles.system.get_parcels(profile_id, GlobalParcel)
    print_parcel_details(parcel_list)
    parcel_list = session.api.sdwan_feature_profiles.system.get_parcels(profile_id, BasicParcel)
    print_parcel_details(parcel_list)
    parcel_list = session.api.sdwan_feature_profiles.system.get_parcels(profile_id, AAAParcel)
    print_parcel_details(parcel_list)
    parcel_list = session.api.sdwan_feature_profiles.system.get_parcels(profile_id, OMPParcel)
    print_parcel_details(parcel_list)
    parcel_list = session.api.sdwan_feature_profiles.system.get_parcels(profile_id, LoggingParcel)
    print_parcel_details(parcel_list)
    parcel_list = session.api.sdwan_feature_profiles.system.get_parcels(profile_id, BFDParcel)
    print_parcel_details(parcel_list)


def print_transport_parcel_details(profile_id: UUID):
    print("not implemented")


def print_service_parcel_details(profile_id: UUID):
    print("not implemented")


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

    system_api = session.api.sdwan_feature_profiles.system
    print_profile_details(system_api)

    transport_api = session.api.sdwan_feature_profiles.transport
    print_profile_details(transport_api)

    service_api = session.api.sdwan_feature_profiles.service
    print_profile_details(service_api)


@click.command()
def get_parcels():
    profile_name = input("Enter Profile Name: ")

    profile = session.api.sdwan_feature_profiles.system.get_profiles().filter(profile_name=profile_name).single_or_default()
    if profile is not None:
        print("~~~ System Profile")
        profile_id = profile.profile_id
        print_system_parcel_details(profile_id)
        exit(0)

    profile = session.api.sdwan_feature_profiles.transport.get_profiles().filter(profile_name=profile_name).single_or_default()
    if profile is not None:
        print("~~~ Transport Profile")
        profile_id = profile.profile_id
        print_transport_parcel_details(profile_id)
        exit(0)

    profile = session.api.sdwan_feature_profiles.service.get_profiles().filter(profile_name=profile_name).single_or_default()
    if profile is not None:
        print("~~~ Service Profile")
        profile_id = profile.profile_id
        print_service_parcel_details(profile_id)
        exit(0)

    print(f"  - Profile does not exist: {profile_name}")


if __name__ == "__main__":
    cli.add_command(get_groups)
    cli.add_command(get_profiles)
    cli.add_command(get_parcels)

    with create_session() as session:
        cli()
