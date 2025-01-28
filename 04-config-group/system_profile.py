import sys
from typing import List, Literal, Optional, Union, cast
from uuid import UUID

import urllib3

sys.path.insert(0, "..")

from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.configuration.feature_profile.sdwan.system import BFDParcel, MRFParcel, OMPParcel
from catalystwan.session import ManagerSession

EnableMrfMigration = Literal["enabled", "enabled-from-bgp-core"]
Role = Literal["edge-router", "border-router"]

# Disable warnings because of no certificate on vManage
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SystemProfile:
    def __init__(self, session: ManagerSession):
        self.session = session
        self.profile_name = "SDK_SystemProfile"
        self.profile_description = "System Profile from SDK"
        self.system_api = self.session.api.sdwan_feature_profiles.system

    def create(self) -> UUID:
        """Create a System Profile with required parcels."""

        print("\nCreating new System Profile")

        # Check if profile exists and delete
        self.delete()

        # Create new System Profile
        profile_id = self.system_api.create_profile(self.profile_name, self.profile_description).id

        print(f"- New System Profile ID: {profile_id}")

        # Create parcels
        self.create_omp_parcel(profile_id)
        self.create_bfd_parcel(profile_id)
        self.create_mrf_parcel(profile_id)

        return profile_id

    def delete(self) -> bool:
        """Delete existing system profile if it exists."""

        existing_profile = self.system_api.get_profiles().filter(profile_name=self.profile_name).single_or_default()

        if existing_profile is not None:
            existing_profile_id = existing_profile.profile_id
            self.system_api.delete_profile(existing_profile_id)
            print(f"- Existing Profile {self.profile_name} deleted: {existing_profile_id}")
            return True

        print(f"- Profile {self.profile_name} not found")
        return False

    def create_omp_parcel(self, profile_id: UUID) -> UUID:
        """Create OMP parcel and attach it to the profile."""

        omp = OMPParcel(parcel_name="SDK_OMP_Parcel", ignore_region_path_length=None, transport_gateway=None, site_types_for_transport_gateway=None)
        omp.holdtime = Global[int](value=60)
        parcel_id = self.system_api.create_parcel(profile_id, omp).id
        print(f"- OMP parcel: {parcel_id}")
        return parcel_id

    def create_bfd_parcel(self, profile_id: UUID) -> UUID:
        """Create BFD parcel and attach it to the profile."""

        bfd = BFDParcel(parcel_name="SDK_BFD_Parcel")
        bfd.poll_interval = Global[int](value=50000)
        parcel_id = self.system_api.create_parcel(profile_id, bfd).id
        print(f"- BFD parcel: {parcel_id}")
        return parcel_id

    def create_mrf_parcel(self, profile_id: UUID) -> UUID:
        """Create MRF parcel and attach it to the profile."""

        mrf = MRFParcel(parcel_name="SDK_MRF_Parcel")
        mrf.role = Global[Role](value="edge-router")
        # mrf.role = as_global("edge-router") # works but generate pydandic warning
        parcel_id = self.system_api.create_parcel(profile_id, mrf).id
        print(f"- MRF parcel: {parcel_id}")
        return parcel_id
