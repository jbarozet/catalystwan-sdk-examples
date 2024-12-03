import json
import os
import sys

sys.path.insert(0, "..")
from utils.session import create_session

# Create payload folder
data_dir = "./payloads/cg/"
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
    print("Folder %s created!" % data_dir)
else:
    print("Folder %s already exists" % data_dir)


# Create session
session = create_session()

# Get list of config groups
url_base = "dataservice/v1/config-group/"
data = session.get(url_base).json()
filename = "".join([data_dir, "1_payload_config_groups.json"])

print("\n~~~ Saving payload in file payload_config_groups.json")
with open(filename, "w") as file:
    json.dump(data, file, indent=4)


# Get list of feature profiles
url_base = "dataservice/v1/feature-profile/sdwan/"
data = session.get(url_base).json()
filename = "".join([data_dir, "2_payload_feature_profiles.json"])

print("\n~~~ Saving payload in file payload_feature_profiles.json")
with open(filename, "w") as file:
    json.dump(data, file, indent=4)

# Get feature profile payloads
for key in data:
    profile_id = key["profileId"]
    profile_type = key["profileType"]

    match profile_type:
        case "system":
            urlp = url_base + "system/"
            url = urlp + profile_id + "?details=true"
            filename = "".join([data_dir, "3_payload_feature_profile", "_system_", profile_id, ".json"])
        case "transport":
            urlp = url_base + "transport/"
            url = urlp + profile_id + "?details=true"
            filename = "".join([data_dir, "4_payload_feature_profile", "_transport_", profile_id, ".json"])
        case "service":
            urlp = url_base + "service/"
            url = urlp + profile_id + "?details=true"
            filename = "".join([data_dir, "5_payload_feature_profile", "_service_", profile_id, ".json"])
        case "cli":
            urlp = url_base + "cli/"
            url = urlp + profile_id + "?details=true"
            filename = "".join([data_dir, "6_payload_feature_profile", "_cli_", profile_id, ".json"])
        case "policy-object":
            urlp = url_base + "policy-object/"
            url = urlp + profile_id
            filename = "".join([data_dir, "7_payload_feature_profile", "_policy_", profile_id, ".json"])
        case _:
            exit(f"{profile_type} type not supported")

    data = session.get(url).json()

    print(f"\n~~~ Saving {profile_id} payload details in {filename}")
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

session.close()
