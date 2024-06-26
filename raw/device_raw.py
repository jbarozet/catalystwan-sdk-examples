import json
import os
import sys

sys.path.insert(0, "..")

from session import create_session

# Create session
session = create_session()

# Get list of devices
url_base = "dataservice/system/device/vedges"
payload = session.get(url_base).json()

# Create payload folder
path = "./payloads"
if not os.path.exists(path):
    os.mkdir(path)
    print("\n~~~ Folder %s created!" % path)
else:
    print("\n~~~ Folder %s already exists" % path)

print("\n~~~ Saving payload in file payloads/payload_devices.json")
with open("payloads/payload_devices.json", "w") as file:
    json.dump(payload, file, indent=4)

session.close()
