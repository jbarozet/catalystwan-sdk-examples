import sys
from typing import Literal

import click
import urllib3

sys.path.insert(0, "..")
from ipaddress import IPv4Address, IPv6Address, IPv6Interface
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_default, as_global, as_variable
from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.common import EncapType, StaticIPv4Address, StaticIPv4AddressConfig
from catalystwan.models.configuration.feature_profile.sdwan.system import BFDParcel, OMPParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import TransportVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    Encapsulation,
    InterfaceDynamicIPv4Address,
    InterfaceEthernetParcel,
    InterfaceStaticIPv4Address,
)
from catalystwan.session import ManagerSession

from utils.session import create_session

# Disable warnings because of no certificate on vManage
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group()
def cli():
    """Command line tool for to manage Configuration Groups, Feature Profiles and Parcels"""
    pass


# --- Delete Config Group -------------------------------------
def delete_config_group(session: ManagerSession):
    config_group_name = "SDK_ConfigGroup"
    print(f"- Searching Config Group: {config_group_name}")
    # Search Config Group
    config_group = session.api.config_group.get().filter(name=config_group_name).single_or_default()
    if config_group is not None:
        config_group_id = config_group.id
        session.api.config_group.delete(config_group_id)
        print(f"- Config Group deleted: {config_group_id}")

    print("- Config Group not found")


# --- Delete System Profile -------------------------------------
def delete_system_profile(session: ManagerSession) -> bool:
    profile_name = "SDK_SystemProfile"
    print(f"- Searching System Profile: {profile_name}")
    existing_profile = session.api.sdwan_feature_profiles.system.get_profiles().filter(profile_name=profile_name).single_or_default()

    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        session.api.sdwan_feature_profiles.system.delete_profile(existing_profile_id)
        print(f"- Profile deleted: {existing_profile_id}")
        return True

    print("- Profile not found")
    return False


# --- Delete Transport Profile -------------------------------------
def delete_transport_profile(session: ManagerSession) -> bool:
    profile_name = "SDK_TransportProfile"
    print(f"- Searching Transport Profile: {profile_name}")
    existing_profile = session.api.sdwan_feature_profiles.transport.get_profiles().filter(profile_name=profile_name).single_or_default()
    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        print(f"- Profile deleted: {existing_profile_id}")
        session.api.sdwan_feature_profiles.transport.delete_profile(existing_profile_id)
        return True

    print("- Profile not found")
    return False


# --- Delete Service Profile -------------------------------------
def delete_service_profile(session: ManagerSession) -> bool:
    profile_name = "SDK_ServiceProfile"
    print(f"- Searching Service Profile: {profile_name}")
    existing_profile = session.api.sdwan_feature_profiles.service.get_profiles().filter(profile_name=profile_name).single_or_default()

    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        session.api.sdwan_feature_profiles.service.delete_profile(existing_profile_id)
        print(f"- Profile deleted: {existing_profile_id}")
        return True

    print("- Profile not found")
    return False


# --- Create System Profile ---------------------------------------------------
def create_system_profile(session: ManagerSession) -> UUID:
    """
    This function creates a System Profile with required parcels
    """

    profile_name = "SDK_SystemProfile"
    profile_description = "System Profile from SDK"

    print(f"- Configuring System Profile: {profile_name}")

    # Check if profile exists and delete
    delete_system_profile(session)

    # Create new System Profile
    profile_id = session.api.sdwan_feature_profiles.system.create_profile(profile_name, profile_description).id
    system_api = session.api.sdwan_feature_profiles.system
    print(f"- New System Profile ID: {profile_id}")

    # Create OMP Parcel
    omp = OMPParcel(parcel_name="SDK_OMP_Parcel")
    omp.holdtime = as_global(value=60)
    # omp.holdtime = as_variable("HoldTime")
    parcel_id = system_api.create_parcel(profile_id, omp).id
    print(f"- OMP parcel: {parcel_id}")

    # Create BFD Parcel
    bfd = BFDParcel(parcel_name="SDK_BFD_Parcel")
    bfd.poll_interval = as_global(50000)
    parcel_id = system_api.create_parcel(profile_id, bfd).id
    print(f"- BFD parcel: {parcel_id}")

    return profile_id


# --- Create Transport Profile ------------------------------------------------
def create_transport_profile(session: ManagerSession) -> UUID:
    """
    This function creates a Transport Profile with required parcels
    """

    profile_name = "SDK_TransportProfile"
    profile_description = "Transport Profile from SDK"

    print(f"- Configuring Transport Profile: {profile_name}")

    # Check if profile exists and delete
    delete_transport_profile(session)

    # --- Create new transport profile
    profile_id = session.api.sdwan_feature_profiles.transport.create_profile(profile_name, profile_description).id
    transport_api = session.api.sdwan_feature_profiles.transport
    print(f"- Transport Profile ID: {profile_id}")

    # --- Create VPN Parcel
    vpn = TransportVpnParcel(parcel_name="SDK_VPN0_Parcel")
    # vpn.vpn_id = as_global(0) # this is a frozen parameter - always 0

    dns1 = as_global(IPv4Address("172.16.1.254"))
    dns2 = as_global(IPv4Address("172.16.2.254"))
    vpn.set_dns_ipv4(dns1, dns2)

    prefix = as_global(IPv4Address("0.0.0.0"))
    mask = as_global("0.0.0.0", generic_alias=SubnetMask)
    next_hops = [
        (as_global(IPv4Address("172.16.1.254")), as_global(1)),
        (as_global(IPv4Address("172.16.2.254")), as_global(8)),
    ]
    vpn.add_ipv4_route(prefix, mask, next_hops)
    vpn_parcel_id = transport_api.create_parcel(profile_id, vpn).id
    print(f"- VPN parcel: {vpn_parcel_id}")

    # Create VPN0 Transport Interfaces
    # encapsulation = Encapsulation(encap=as_global("ipsec", Literal["ipsec", "gre"]))
    # encapsulation = [Encapsulation()]
    interface_name = as_global("GigabitEthernet1")
    encap_value = Global[Literal["ipsec", "gre"]](option_type="global", value="ipsec")
    encapsulation = Encapsulation(encap=encap_value, preference=as_global(100), weight=as_global(1))

    interface_ip_address = InterfaceStaticIPv4Address(
        static=StaticIPv4AddressConfig(
            primary_ip_address=StaticIPv4Address(ip_address=as_global(IPv4Address("172.16.1.1")), subnet_mask=as_global("255.255.255.0"))
        )
    )
    interface_description = as_global("mpls")
    interface_shutdown = as_global(True)
    interface_parcel = InterfaceEthernetParcel(
        parcel_name="SDK_VPN0_Interface_mpls_Parcel",
        encapsulation=[encapsulation],
        interface_name=interface_name,
        interface_ip_address=interface_ip_address,
        interface_description=interface_description,
        shutdown=interface_shutdown,
    )

    interface_parcel_id = session.api.sdwan_feature_profiles.transport.create_parcel(profile_id, interface_parcel, vpn_uuid=vpn_parcel_id).id
    print(f"- VPN Interface parcel: {interface_parcel_id}")

    return profile_id


# --- Create Service Profile --------------------------------------------------
def create_service_profile(session: ManagerSession) -> UUID:
    """
    This function creates a Service Profile with required parcels
    """

    profile_name = "SDK_ServiceProfile"
    profile_description = "Service Profile from SDK"

    print(f"- Configuring Service Profile: {profile_name}")

    # Check if profile exists and delete
    delete_service_profile(session)

    profile_id = session.api.sdwan_feature_profiles.service.create_profile(profile_name, profile_description).id
    service_api = session.api.sdwan_feature_profiles.service
    print(f"- Service Profile ID: {profile_id}")

    return profile_id


# --- Create Config Group -----------------------------------------------------
def create_config_group(
    session: ManagerSession,
    system_profile_id: UUID,
    transport_profile_id: UUID,
    service_profile_id: UUID,
) -> UUID:
    """
    This function creates a Configuration Group with associated profiles
    """

    config_group_name = "SDK_ConfigGroup"
    config_group_description = "Config Group from SDK"
    config_group_solution = "sdwan"

    print(f"- Configuring Config Group: {config_group_name}")

    config_group_id = session.api.config_group.create(
        name=config_group_name,
        description=config_group_description,
        solution=config_group_solution,
        profile_ids=[
            system_profile_id,
            transport_profile_id,
            service_profile_id,
        ],
    ).id

    return config_group_id


# --- Command: delete ---------------------------------------------------------
@click.command()
def delete():
    with create_session() as session:
        # Delete config group
        delete_config_group(session)
        # Delete associated profiles
        delete_system_profile(session)
        delete_transport_profile(session)
        delete_service_profile(session)


# --- Command: Create ---------------------------------------------------------
@click.command()
def create():
    with create_session() as session:
        # Configure Feature Profiles
        system_profile_id = create_system_profile(session)
        transport_profile_id = create_transport_profile(session)
        service_profile_id = create_service_profile(session)
        # Configure Config Group
        config_group_id = create_config_group(session, system_profile_id, transport_profile_id, service_profile_id)
        # Summary
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
