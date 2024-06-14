import json
import os
import sys

sys.path.insert(0, "..")

from session import create_session

# Create payload folder
path = "./payloads"
if not os.path.exists(path):
    os.mkdir(path)
    print("Folder %s created!" % path)
else:
    print("Folder %s already exists" % path)


# Create session
session = create_session()

# Get list of config groups
url_base = "dataservice/v1/config-group/"
data = session.get(url_base).json()

print("\n~~~ Saving payload in file payload_config_groups.json")
with open("payloads/payload_config_groups.json", "w") as file:
    json.dump(data, file, indent=4)


# Get list of feature profiles
url_base = "dataservice/v1/feature-profile/sdwan/"
data = session.get(url_base).json()

print("\n~~~ Saving payload in file payload_feature_profiles.json")
with open("payloads/payload_feature_profiles.json", "w") as file:
    json.dump(data, file, indent=4)

# Get feature profile payloads
for key in data:
    profile_id = key["profileId"]
    profile_type = key["profileType"]

    match profile_type:
        case "system":
            urlp = url_base + "system/"
        case "transport":
            urlp = url_base + "transport/"
        case "service":
            urlp = url_base + "service/"
        case "cli":
            urlp = url_base + "cli/"
        case "policy-object":
            urlp = url_base + "policy-object/"
        case _:
            exit(f"{profile_type} type not supported")

    url = urlp + profile_id + "?details=true"
    data = session.get(url).json()
    filename = "".join(["payloads/", "payload_feature_profile_", profile_id, ".json"])
    print(f"\n~~~ Saving {profile_id} payload details in {filename}")
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

session.close()
