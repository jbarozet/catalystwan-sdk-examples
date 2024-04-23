"""
Catalyst SD-WAN Manager SDK - Config Groups and Feature Profiles
"""

# export catalystwan_devel=true

import urllib3

from session import create_session

# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create vManage session
session = create_session()

# Get the list of config_groups
config_groups = session.api.config_group.get()

# Display the list of config_groups
for group in config_groups:
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Config Group Name: {group.name}")
    print(f"- Description: {group.description}")
    print(f"- Solution: {group.solution}")

    for profile in group.profiles:
        print(f"- Profile Id: {profile.id}")
        print(f"  - Name: {profile.name}")
        print(f"  - Type: {profile.type}")
        print(f"  - Solution: {profile.solution}")
        print(f"  - Created by: {profile.created_by}")
        print(f"  - Last updated by: {profile.last_updated_by}")
        print(f"  - Last updated on: {profile.last_updated_on}")

profiles = session.api.sd_routing_feature_profiles.cli.endpoint.get_cli_feature_profiles()
for item in profiles:
    print(f"\nProfile Id: {item.profile_id}")
    print(f"  - Profile Name: {item.profile_name}")
    print(f"  - Solution: {item.solution}")
    print(f"  - Type: {item.profile_type}")

profiles = session.api.sdwan_feature_profiles.system.get_profiles()
for item in profiles:
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"SDWAN Profile Id: {item.profile_id}")
    print(f"  - Profile Name: {item.profile_name}")
    print(f"  - Solution: {item.solution}")
    print(f"  - Type: {item.profile_type}")

# parcels = session.api.sdwan_feature_profiles.system.get_parcels(
#     profile_id="4a53c92c-17b2-4804-9563-b9144a8fac22", parcel_type="AAA"
# )
# print(parcels)


# ---END--
