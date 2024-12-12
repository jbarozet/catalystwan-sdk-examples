import sys
from typing import cast

import urllib3

sys.path.insert(0, "..")
from uuid import UUID

# Default, Global, Variable, as_default, as_global, as_variable
from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.configuration.feature_profile.sdwan.system import BFDParcel, OMPParcel
from catalystwan.session import ManagerSession

# Disable warnings because of no certificate on vManage
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# --- Delete System Profile -------------------------------------
def delete_system_profile(session: ManagerSession) -> bool:
    profile_name = "SDK_SystemProfile"
    existing_profile = session.api.sdwan_feature_profiles.system.get_profiles().filter(profile_name=profile_name).single_or_default()

    if existing_profile is not None:
        existing_profile_id = existing_profile.profile_id
        session.api.sdwan_feature_profiles.system.delete_profile(existing_profile_id)
        print(f"- Existing Profile {profile_name} deleted: {existing_profile_id}")
        return True

    print(f"- Profile {profile_name} not found")
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
    omp = OMPParcel(parcel_name="SDK_OMP_Parcel", ignore_region_path_length=None, transport_gateway=None, site_types_for_transport_gateway=None)
    # omp.holdtime = cast(Global[int], as_global(value=60))
    omp.holdtime = Global(value=60)
    # omp.holdtime = as_variable("HoldTime")
    parcel_id = system_api.create_parcel(profile_id, omp).id
    print(f"- OMP parcel: {parcel_id}")

    # Create BFD Parcel
    bfd = BFDParcel(parcel_name="SDK_BFD_Parcel")
    bfd.poll_interval = Global(value=50000)
    parcel_id = system_api.create_parcel(profile_id, bfd).id
    print(f"- BFD parcel: {parcel_id}")

    return profile_id
