# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Device Config
# Using Config Group and Feature Profiles
#
# =========================================================================

from logging import Manager
import sys
from rich import print
from rich.console import Console
from rich.pretty import Pretty
from rich.panel import Panel
from uuid import UUID

import click
from tabulate import tabulate

from catalystwan.session import ManagerSession

from catalystwan.models.configuration.feature_profile.common import FeatureProfileInfo
from catalystwan.models.configuration.feature_profile.sdwan.system.aaa import AAAParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.basic import BasicParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.bfd import BFDParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.global_parcel import GlobalParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.logging_parcel import LoggingParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.omp import OMPParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.banner import BannerParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.snmp import SNMPParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.ntp import NtpParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.mrf import MRFParcel
from catalystwan.typed_list import DataSequence

sys.path.insert(0, "..")
from utils.session import create_session


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


# --- Get parcels -------------------------------------------------------


def print_parcel_details(parcel_type, parcel):
    if parcel is None:
        print(f"** Parcel: {parcel_type}: none")
    else:
        print(f"** Parcel: {parcel.parcel_type}")
        print(f"  - id: {parcel.parcel_id}")
        print(f"  - name: {parcel.payload.parcel_name}")
        print(f"  - description: {parcel.payload.parcel_description}")
        # print(f"  - Payload: {parcel.payload.model_dump_json(by_alias=True, indent=4)}")

    # to display the parcel object and all parameters
    # Also display all parcel types for this profile type
    # console = Console()
    # console.print(Panel(Pretty(parcel), title="API Response", expand=False))


def print_system_parcel_details(session: ManagerSession, profile_id: UUID) -> None:
    """Prints system parcel details for a given profile ID."""
    parcel_classes = [
        ("Global", GlobalParcel),
        ("Basic", BasicParcel),
        ("AAA", AAAParcel),
        ("OMP", OMPParcel),
        ("Logging", LoggingParcel),
        ("BFD", BFDParcel),
        ("Banner", BannerParcel),
        ("NTP", NtpParcel),
        ("SNMP", SNMPParcel),
        ("MRF", MRFParcel),
    ]

    for parcel_type, parcel_class in parcel_classes:
        parcel = session.api.sdwan_feature_profiles.system.get_parcels(profile_id, parcel_class).single_or_default()
        print_parcel_details(parcel_type, parcel)


def print_transport_parcel_details(session: ManagerSession, profile_id: UUID):
    print("not implemented")


def print_service_parcel_details(session: ManagerSession, profile_id: UUID):
    print("not implemented")


@click.command()
def get_parcels():
    profile_name = input("Enter Profile Name: ")

    with create_session() as session:
        profile_types = {
            "System": {
                "api_method": session.api.sdwan_feature_profiles.system.get_profiles,
                "print_function": print_system_parcel_details,
                "label": "~~~ System Profile",
            },
            "Transport": {
                "api_method": session.api.sdwan_feature_profiles.transport.get_profiles,
                "print_function": print_transport_parcel_details,
                "label": "~~~ Transport Profile",
            },
            "Service": {
                "api_method": session.api.sdwan_feature_profiles.service.get_profiles,
                "print_function": print_service_parcel_details,
                "label": "~~~ Service Profile",
            },
        }

        for profile_type, config in profile_types.items():
            profile = config["api_method"]().filter(profile_name=profile_name).single_or_default()
            if profile is not None:
                print(config["label"])
                config["print_function"](session, profile.profile_id)
                return

        print(f"Profile does not exist: {profile_name}")


# --- Get profiles ----------------------------------


def print_profile_details(profile_list: DataSequence[FeatureProfileInfo]):
    if profile_list is not None:
        table = list()
        headers = ["Name", "Type", "Solution", "ID", "Created by", "Last Updated by", "Last updated on"]

        for profile in profile_list:
            tr = [
                profile.profile_name,
                profile.profile_type,
                profile.solution,
                profile.profile_id,
                profile.created_by,
                profile.last_updated_by,
                profile.last_updated_on,
            ]
            table.append(tr)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def get_profiles():
    with create_session() as session:
        print("System Profiles:")
        system_profile_list = session.api.sdwan_feature_profiles.system.get_profiles()
        print_profile_details(system_profile_list)

        print("\nTransport Profiles:")
        transport_profile_list = session.api.sdwan_feature_profiles.transport.get_profiles()
        print_profile_details(transport_profile_list)

        print("\nService Profiles:")
        service_profile_list = session.api.sdwan_feature_profiles.service.get_profiles()
        print_profile_details(service_profile_list)


# ---- Get config-groups -----------------------


@click.command()
def get_groups():
    print("\n~~~ List of Configuration Groups\n")

    with create_session() as session:
        config_groups = session.api.config_group.get()

        for group in config_groups:
            print(f"\nConfig Group Name: {group.name}")
            print(f"- Description: {group.description}")
            print(f"- Solution: {group.solution}")

            table = list()
            headers = ["Name", "Type", "Solution", "ID", "Created by", "Last Updated by", "Last updated on"]

            profile_list = group.profiles

            if profile_list is not None:
                for profile in profile_list:
                    tr = [
                        profile.name,
                        profile.type,
                        profile.solution,
                        profile.id,
                        profile.created_by,
                        profile.last_updated_by,
                        profile.last_updated_on,
                    ]
                    table.append(tr)

                click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    cli.add_command(get_groups)
    cli.add_command(get_profiles)
    cli.add_command(get_parcels)
    cli()
