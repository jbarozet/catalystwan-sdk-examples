import sys
from typing import Literal
import urllib3
from uuid import UUID
from ipaddress import IPv4Address, IPv6Address, IPv6Interface

sys.path.insert(0, "..")

from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.common import StaticIPv4Address, StaticIPv4AddressConfig
from catalystwan.session import ManagerSession


# Disable warnings because of no certificate on vManage
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ServiceProfile:
    def __init__(self, session: ManagerSession):
        self.session = session
        self.profile_name = "SDK_ServiceProfile"
        self.profile_description = "Service Profile from SDK"
        self.service_api = self.session.api.sdwan_feature_profiles.service

    def delete(self) -> bool:
        """Delete existing service profile if it exists."""
        existing_profile = self.service_api.get_profiles().filter(profile_name=self.profile_name).single_or_default()

        if existing_profile is not None:
            existing_profile_id = existing_profile.profile_id
            self.service_api.delete_profile(existing_profile_id)
            print(f"- Existing Profile {self.profile_name} deleted: {existing_profile_id}")
            return True

        print(f"- Profile {self.profile_name} not found")
        return False

    def create(self) -> UUID:
        """Create a Service Profile with required parcels."""

        print("\nCreating new Service Profile")

        # Check if profile exists and delete
        self.delete()

        # Create new Service Profile
        profile_id = self.service_api.create_profile(self.profile_name, self.profile_description).id
        print(f"- New Service Profile ID: {profile_id}")

        # Add any additional parcel creation methods here if needed
        # self.create_parcel_1(profile_id)
        # self.create_parcel_2(profile_id)

        return profile_id


# Usage example:
# session = ManagerSession(...)
# service_manager = ServiceProfileManager(session)
# profile_id = service_manager.create_service_profile()
