import sys
from typing import Literal

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


# Configure System Profile
def configure_system_profile(session: ManagerSession) -> UUID:
    """
    This function creates a System Profile with required parcels
    """

    profile_name = "SDK_SystemProfile"
    profile_description = "System Profile from SDK"

    print(f"~~~ Configuring System Profile: {profile_name}")

    existing_profile = session.api.sdwan_feature_profiles.system.get_profiles().filter(profile_name=profile_name).single_or_default()

    # Check there is no existing template with the same name
    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        print(f"  - Profile already exist: {existing_profile_id}")
        session.api.sdwan_feature_profiles.system.delete_profile(existing_profile_id)
        print("  - profile deleted")

    # Create new System Profile
    profile_id = session.api.sdwan_feature_profiles.system.create_profile(profile_name, profile_description).id
    system_api = session.api.sdwan_feature_profiles.system
    print(f"  - New System Profile ID: {profile_id}")

    # Create OMP Parcel
    omp = OMPParcel(parcel_name="SDK_OMP_Parcel")
    omp.holdtime = Global(value=60)
    # omp.holdtime = as_variable("HoldTime")
    omp.holdtime = Global(value=40)
    parcel_id = system_api.create_parcel(profile_id, omp).id
    print(f"  - OMP parcel: {parcel_id}")

    # Create BFD Parcel
    bfd = BFDParcel(parcel_name="SDK_BFD_Parcel")
    bfd.poll_interval = as_global(50000)
    parcel_id = system_api.create_parcel(profile_id, bfd).id
    print(f"  - BFD parcel: {parcel_id}")

    return profile_id


def configure_transport_profile(session: ManagerSession) -> UUID:
    """
    This function creates a Transport Profile with required parcels
    """

    profile_name = "SDK_TransportProfile"
    profile_description = "Transport Profile from SDK"

    print(f"~~~ Configuring Transport Profile: {profile_name}")

    # Check there is no existing template with the same name
    existing_profile = session.api.sdwan_feature_profiles.transport.get_profiles().filter(profile_name=profile_name).single_or_default()

    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        print(f"  - Profile already exist: {existing_profile_id}")
        print("  - profile deleted")
        session.api.sdwan_feature_profiles.transport.delete_profile(existing_profile_id)

    # --- Create new transport profile
    profile_id = session.api.sdwan_feature_profiles.transport.create_profile(profile_name, profile_description).id
    transport_api = session.api.sdwan_feature_profiles.transport
    print(f"  - Transport Profile ID: {profile_id}")

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
    print(f"  - VPN parcel: {vpn_parcel_id}")

    # Create VPN0 Transport Interfaces
    # encapsulation = Encapsulation(encap=as_global("ipsec", Literal["ipsec", "gre"]))
    # encapsulation = [Encapsulation()]
    interface_name = as_global("GigabitEthernet1")
    # encapsulation = Encapsulation(encap=as_global("ipsec"))
    encap_global = Global[Literal["ipsec", "gre"]](option_type="global", value="ipsec")
    encap_config = Encapsulation(encap=encap_global)

    # encapsulation = Encapsulation(
    #     encap=as_global(EncapType.IPSEC),
    #     preference=as_global(1),  # if you need to set preference
    #     weight=as_global(1),  # if you need to set weight
    # )

    interface_ip_address = InterfaceStaticIPv4Address(
        static=StaticIPv4AddressConfig(
            primary_ip_address=StaticIPv4Address(ip_address=as_global(IPv4Address("172.16.1.1")), subnet_mask=as_global("255.255.255.0"))
        )
    )
    interface_description = as_global("mpls")
    interface_shutdown = as_global(True)
    interface_parcel = InterfaceEthernetParcel(
        parcel_name="SDK_VPN0_Interface_mpls_Parcel",
        encapsulation=[encap_config],
        interface_name=interface_name,
        interface_ip_address=interface_ip_address,
        interface_description=interface_description,
        shutdown=interface_shutdown,
    )

    interface_parcel_id = session.api.sdwan_feature_profiles.transport.create_parcel(profile_id, interface_parcel, vpn_uuid=vpn_parcel_id).id
    print(f"  - VPN parcel: {interface_parcel_id}")

    return profile_id


def configure_service_profile(session: ManagerSession) -> UUID:
    """
    This function creates a Service Profile with required parcels
    """

    profile_name = "SDK_ServiceProfile"
    profile_description = "Service Profile from SDK"

    print(f"~~~ Configuring Service Profile: {profile_name}")

    # Check there is no existing template with the same name
    existing_profile = session.api.sdwan_feature_profiles.service.get_profiles().filter(profile_name=profile_name).single_or_default()

    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        print(f"  - Profile already exist: {existing_profile_id}")
        print("  - profile deleted")
        session.api.sdwan_feature_profiles.service.delete_profile(existing_profile_id)

    profile_id = session.api.sdwan_feature_profiles.service.create_profile(profile_name, profile_description).id
    service_api = session.api.sdwan_feature_profiles.service
    print(f"  - New Service Profile ID: {profile_id}")

    return profile_id


def configure_group(
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

    print(f"~~~ Configuring Config Group: {config_group_name}")

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


def run_demo():
    with create_session() as session:
        system_profile_id = configure_system_profile(session)
        transport_profile_id = configure_transport_profile(session)
        service_profile_id = configure_service_profile(session)

        config_group_id = configure_group(session, system_profile_id, transport_profile_id, service_profile_id)

        print("\n~~~ Summary")
        print("  - ConfigGroup ID:", config_group_id)
        print("  - System Profile ID:", system_profile_id)
        print("  - Transport Profile ID:", transport_profile_id)
        print("  - Service Profile ID:", service_profile_id)

        # Cleanup
        input("Press Enter to delete Config Group and Feature Profiles: ")
        session.api.config_group.delete(config_group_id)
        session.api.sdwan_feature_profiles.system.delete_profile(system_profile_id)
        session.api.sdwan_feature_profiles.transport.delete_profile(transport_profile_id)
        session.api.sdwan_feature_profiles.service.delete_profile(service_profile_id)


if __name__ == "__main__":
    run_demo()
