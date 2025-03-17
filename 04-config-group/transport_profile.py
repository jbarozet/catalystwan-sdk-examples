import sys
from ipaddress import IPv4Address
from typing import List, Literal
from uuid import UUID

import urllib3

# from catalystwan.api.templates.models.cisco_vpn_interface_model import CoreRegion
# from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.t1e1serial import MultiRegionFabric

sys.path.insert(0, "..")

from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.common import CoreRegion, SubnetMask
from catalystwan.models.configuration.feature_profile.common import EncapType, MultiRegionFabric, StaticIPv4Address, StaticIPv4AddressConfig
from catalystwan.models.configuration.feature_profile.sdwan.transport import TransportVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    Encapsulation,
    InterfaceEthernetParcel,
    InterfaceStaticIPv4Address,
    Tunnel,
)
from catalystwan.session import ManagerSession

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TransportProfile:
    def __init__(self, session: ManagerSession):
        self.session = session
        self.profile_name = "SDK_TransportProfile"
        self.profile_description = "Transport Profile from SDK"
        self.transport_api = self.session.api.sdwan_feature_profiles.transport

    # --- Create Profile ----------------------------------
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
        self.create_interface_parcels(profile_id, vpn_parcel_id)

        return profile_id

    # --- Delete Profile ----------------------------------
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

    # --- Create VPN Parcel ----------------------------------
    def create_vpn_parcel(self, profile_id: UUID) -> UUID:
        """Create VPN0 parcel and configure DNS and routes."""

        # Define VPN configuration
        vpn_config = {
            "parcel_name": "SDK_VPN0_Parcel",
            "dns": {"primary": "172.16.1.254", "secondary": "172.16.2.254"},
            "routes": [
                {
                    "prefix": "0.0.0.0",
                    "mask": "0.0.0.0",
                    "next_hops": [{"address": "172.16.1.254", "distance": 1}, {"address": "172.16.2.254", "distance": 8}],
                }
            ],
        }

        # Create VPN parcel
        vpn = TransportVpnParcel(parcel_name=vpn_config["parcel_name"])

        # Configure DNS
        dns1 = as_global(IPv4Address(vpn_config["dns"]["primary"]))
        dns2 = as_global(IPv4Address(vpn_config["dns"]["secondary"]))
        vpn.set_dns_ipv4(dns1, dns2)

        # Configure routes
        for route in vpn_config["routes"]:
            prefix = as_global(IPv4Address(route["prefix"]))
            mask = as_global(route["mask"], generic_alias=SubnetMask)
            next_hops = [(as_global(IPv4Address(hop["address"])), as_global(hop["distance"])) for hop in route["next_hops"]]
            vpn.add_ipv4_route(prefix, mask, next_hops)

        # Create the parcel
        vpn_parcel_id = self.transport_api.create_parcel(profile_id, vpn).id
        print(f"- VPN0 parcel: {vpn_parcel_id}")
        return vpn_parcel_id

    # --- Create WAN Interface Parcels ----------------------------------
    def create_interface_parcels(self, profile_id: UUID, vpn_parcel_id: UUID) -> List[UUID]:
        """Create multiple VPN0 Transport Interface parcels."""

        # Define interface configurations
        interface_configs = [
            {
                "parcel_name": "SDK_VPN0_Interface_internet_Parcel",
                "interface_name": "GigabitEthernet1",
                "ip_address": "172.16.1.1",
                "subnet_mask": "255.255.255.0",
                "description": "internet",
                "encap": "ipsec",
                "preference": 100,
                "weight": 1,
                "shutdown": True,
                "tunnel": True,
                "tunnel_config": {
                    "color": "biz-internet",
                    "max_control_connections": 2,
                    "hello_interval": 1000,
                    "hello_tolerance": 12,
                    "border": False,
                },
                "enable_core_region": True,
            },
            {
                "parcel_name": "SDK_VPN0_Interface_mpls_Parcel",
                "interface_name": "GigabitEthernet2",
                "ip_address": "192.168.2.1",
                "subnet_mask": "255.255.255.0",
                "description": "mpls",
                "encap": "ipsec",
                "preference": 200,
                "weight": 1,
                "shutdown": False,
                "tunnel": True,
                "tunnel_config": {
                    "color": "mpls",
                    "max_control_connections": 2,
                    "hello_interval": 1000,
                    "hello_tolerance": 12,
                    "border": False,
                },
                "enable_core_region": False,
            },
        ]

        parcel_ids = []

        for config in interface_configs:
            # Configure interface name
            interface_name = Global[str](value=config["interface_name"])
            interface_description = Global(value=config["description"])
            shutdown = Global(value=config["shutdown"])

            # Configure encapsulation
            encap_value = Global[Literal["ipsec", "gre"]](option_type="global", value=config["encap"])
            preference = Global[int](value=config["preference"])
            weight = Global[int](value=config["weight"])
            encapsulation = Encapsulation(encap=encap_value, preference=preference, weight=weight)

            # Configure interface IP
            ip_address = Global[IPv4Address](value=IPv4Address(config["ip_address"]))
            subnet_mask = Global(value=config["subnet_mask"])
            primary_ip_address = StaticIPv4Address(ip_address=ip_address, subnet_mask=subnet_mask)
            interface_ip_address = InterfaceStaticIPv4Address(static=StaticIPv4AddressConfig(primary_ip_address=primary_ip_address))

            # Configure tunnel
            tunnel_interface = Global(value=config["tunnel"])
            tunnel = Tunnel(
                color=Global(value=config["tunnel_config"]["color"]),
                max_control_connections=Global(value=config["tunnel_config"]["max_control_connections"]),
                hello_interval=Global(value=config["tunnel_config"]["hello_interval"]),
                hello_tolerance=Global(value=config["tunnel_config"]["hello_tolerance"]),
                border=Global(value=config["tunnel_config"]["border"]),
            )

            # Multi-Region Fabric - Enable interface to core
            mrf = MultiRegionFabric()
            # mrf.core_region = Global[CoreRegion](value="core")
            mrf.enable_core_region = Global[bool](value=config["enable_core_region"])

            # Create interface parcel
            interface_parcel = InterfaceEthernetParcel(
                parcel_name=config["parcel_name"],
                encapsulation=[encapsulation],
                interface_name=interface_name,
                interface_ip_address=interface_ip_address,
                interface_description=interface_description,
                shutdown=shutdown,
                tunnel_interface=tunnel_interface,
                tunnel=tunnel,
                multi_region_fabric=mrf,
            )

            interface_parcel_id = self.transport_api.create_parcel(profile_id, interface_parcel, vpn_uuid=vpn_parcel_id).id
            print(f"- VPN0 Interface parcel: {interface_parcel_id} {config["interface_name"]}")
            parcel_ids.append(interface_parcel_id)

        return parcel_ids
