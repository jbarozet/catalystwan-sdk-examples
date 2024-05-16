import urllib3

from session import create_session

# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create vManage session
session = create_session()


system_fp_id = session.api.sdwan_feature_profiles.system.create_profile(
    "SDK - System", "System feature profile (SDK)"
).id

# session.api.config_group.create(name=sd-routing,description="a basic config-group", solution="text", profile_ids=list)
session.api.config_group.create("SDK - Config-Group", "Test Config Group description (SDK)", "sdwan", [system_fp_id])
