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
config_groups = session.endpoints.configuration_group.get()
print(config_groups)


# ---END--
