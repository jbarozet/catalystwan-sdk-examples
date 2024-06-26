import sys

import urllib3

sys.path.insert(0, "..")
from session import create_session

# with create_manager_session(**login, logger=logger) as session:
#     session.api.config_group.get()
#     session.api.config_group.create("test_cg", "description", "sdwan")

# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create vManage session
session = create_session()

# Create Config Group with System Profile
fp_id = session.api.sdwan_feature_profiles.system.create_profile("SystemFeatureProfile", "Description").id
cg_id = session.api.config_group.create(
    name="ConfigGroupName", description="Description", solution="sdwan", profile_ids=[fp_id]
).id
print("ConfigGroup ID:", cg_id)
print("FeatureProfile ID:", fp_id)

# Cleanup
input("Press Enter to delete the ConfigGroup and FeatureProfile: ")
session.api.config_group.delete(cg_id)
session.api.sdwan_feature_profiles.system.delete_profile(fp_id)
