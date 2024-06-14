import sys

sys.path.insert(0, "..")
from session import create_session

# Create session
session = create_session()

# ----------------------------------------------------------------------------------------------------
# Endpoints - Settings
# ----------------------------------------------------------------------------------------------------

settings = session.endpoints.configuration_settings
# Output of get_organisations is in the form of:
# Organization(
#     org: cml-sdwan-lab-tool,
#     domain_id: None,
#     control_connection_up: True,
# )

organizations = settings.get_organizations()

org_name = settings.get_organizations()[0].org
validator_fqdn = settings.get_devices()[0].domain_ip
print(f"Organization Name: {org_name}")
print(settings.get_devices())

session.close()
