import sys
from typing import Literal

import click
import urllib3

sys.path.insert(0, "..")
from ipaddress import IPv4Address, IPv6Address, IPv6Interface
from uuid import UUID

from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.common import StaticIPv4Address, StaticIPv4AddressConfig
from catalystwan.session import ManagerSession

# Disable warnings because of no certificate on vManage
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# --- Delete Service Profile -------------------------------------
def delete_service_profile(session: ManagerSession) -> bool:
    profile_name = "SDK_ServiceProfile"
    existing_profile = session.api.sdwan_feature_profiles.service.get_profiles().filter(profile_name=profile_name).single_or_default()

    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        session.api.sdwan_feature_profiles.service.delete_profile(existing_profile_id)
        print(f"- Existing Profile {profile_name} deleted: {existing_profile_id}")
        return True

    print(f"- Profile {profile_name} not found")
    return False


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
