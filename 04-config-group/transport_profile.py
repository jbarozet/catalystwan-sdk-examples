import sys
from ipaddress import IPv4Address
from typing import Literal
from uuid import UUID

import urllib3

sys.path.insert(0, "..")

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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TransportProfile:
    def __init__(self, session: ManagerSession):
        self.session = session
        self.profile_name = "SDK_TransportProfile"
        self.profile_description = "Transport Profile from SDK"
        self.transport_api = self.session.api.sdwan_feature_profiles.transport

    def create(self) -> UUID:
        """Create a Transport Profile with required parcels."""

        print("\nCreating new Transport Profile")

        # Check if profile exists and delete
        self.delete()

        # Create new Transport Profile
        profile_id = self.transport_api.create_profile(self.profile_name, self.profile_description).id
        print(f"- New Transport Profile ID: {profile_id}")

        # Create VPN and Interface parcels
        vpn_parcel_id = self.create_vpn_parcel(profile_id)
        self.create_interface_parcel(profile_id, vpn_parcel_id)

        return profile_id

    def delete(self) -> bool:
        """Delete existing transport profile if it exists."""
        existing_profile = self.transport_api.get_profiles().filter(profile_name=self.profile_name).single_or_default()

        if existing_profile is not None:
            existing_profile_id = existing_profile.profile_id
            self.transport_api.delete_profile(existing_profile_id)
            print(f"- Existing Profile {self.profile_name} deleted: {existing_profile_id}")
            return True

        print(f"- Profile {self.profile_name} not found")
        return False

    def create_vpn_parcel(self, profile_id: UUID) -> UUID:
        """Create VPN0 parcel and configure DNS and routes."""
        vpn = TransportVpnParcel(parcel_name="SDK_VPN0_Parcel")

        # Configure DNS
        dns1 = as_global(IPv4Address("172.16.1.254"))
        dns2 = as_global(IPv4Address("172.16.2.254"))
        vpn.set_dns_ipv4(dns1, dns2)

        # Configure routes
        prefix = as_global(IPv4Address("0.0.0.0"))
        mask = as_global("0.0.0.0", generic_alias=SubnetMask)
        next_hops = [
            (as_global(IPv4Address("172.16.1.254")), as_global(1)),
            (as_global(IPv4Address("172.16.2.254")), as_global(8)),
        ]
        vpn.add_ipv4_route(prefix, mask, next_hops)

        vpn_parcel_id = self.transport_api.create_parcel(profile_id, vpn).id
        print(f"- VPN parcel: {vpn_parcel_id}")
        return vpn_parcel_id

    def create_interface_parcel(self, profile_id: UUID, vpn_parcel_id: UUID) -> UUID:
        """Create VPN0 Transport Interface parcel."""
        interface_name = as_global("GigabitEthernet1")

        # Configure encapsulation
        encap_value = Global[Literal["ipsec", "gre"]](option_type="global", value="ipsec")
        preference = Global[int](value=100)
        weight = Global[int](value=1)
        encapsulation = Encapsulation(encap=encap_value, preference=preference, weight=weight)

        # Configure interface IP
        interface_ip_address = InterfaceStaticIPv4Address(
            static=StaticIPv4AddressConfig(
                primary_ip_address=StaticIPv4Address(ip_address=as_global(IPv4Address("172.16.1.1")), subnet_mask=as_global("255.255.255.0"))
            )
        )

        # Create interface parcel
        interface_parcel = InterfaceEthernetParcel(
            parcel_name="SDK_VPN0_Interface_mpls_Parcel",
            encapsulation=[encapsulation],
            interface_name=interface_name,
            interface_ip_address=interface_ip_address,
            interface_description=as_global("mpls"),
            shutdown=as_global(True),
        )

        interface_parcel_id = self.transport_api.create_parcel(profile_id, interface_parcel, vpn_uuid=vpn_parcel_id).id
        print(f"- VPN Interface parcel: {interface_parcel_id}")
        return interface_parcel_id
