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


# --- Delete Config Group -------------------------------------
def delete_config_group(session: ManagerSession):
    config_group_name = "SDK_ConfigGroup"
    config_group = session.api.config_group.get().filter(name=config_group_name).single_or_default()

    if config_group is not None:
        config_group_id = config_group.id
        session.api.config_group.delete(config_group_id)
        print(f"- Existing Config Group {config_group_name} deleted: {config_group_id}")

    print(f"- Config Group {config_group_name} not found")


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
