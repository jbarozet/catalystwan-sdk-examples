import json

from session import create_session

# Create session
session = create_session()

url_base = "dataservice/system/device/vedges"
# url_base = "dataservice/v1/feature-profile/sdwan/"
# Get list of profiles
data = session.get(url_base).json()

print("\n~~~ Saving payload in file payload.log")
with open("payload.log", "w") as file:
    json.dump(data, file, indent=4)
