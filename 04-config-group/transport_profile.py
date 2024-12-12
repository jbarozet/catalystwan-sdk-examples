import sys
from typing import Literal, cast

import click
import urllib3

sys.path.insert(0, "..")
from ipaddress import IPv4Address
from uuid import UUID

# Default, Global, Variable, as_default, as_global, as_variable
from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.common import EncapType, StaticIPv4Address, StaticIPv4AddressConfig
from catalystwan.models.configuration.feature_profile.sdwan.transport import TransportVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    Encapsulation,
    InterfaceEthernetParcel,
    InterfaceStaticIPv4Address,
)
from catalystwan.session import ManagerSession

# Disable warnings because of no certificate on vManage
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# --- Delete Transport Profile -------------------------------------
def delete_transport_profile(session: ManagerSession) -> bool:
    profile_name = "SDK_TransportProfile"
    existing_profile = session.api.sdwan_feature_profiles.transport.get_profiles().filter(profile_name=profile_name).single_or_default()

    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        print(f"- Existing Profile {profile_name} deleted: {existing_profile_id}")
        session.api.sdwan_feature_profiles.transport.delete_profile(existing_profile_id)
        return True

    print(f"- Profile {profile_name} not found")
    return False


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
