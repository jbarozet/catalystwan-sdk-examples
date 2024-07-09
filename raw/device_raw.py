import json
import os
import sys

sys.path.insert(0, "..")
from utils.session import create_session

# Create session
session = create_session()

# Get list of devices
url_base = "dataservice/system/device/vedges"
payload = session.get(url_base).json()
devices = payload["data"]  # Get rid of header section and only keep data

# Create payload folder
path = "./payloads"
if not os.path.exists(path):
    os.mkdir(path)
    print("\n~~~ Folder %s created!" % path)
else:
    print("\n~~~ Folder %s already exists" % path)

# Dump devices to json
print("\n~~~ Saving payload in file payloads/payload_devices.json")
with open("payloads/payload_devices.json", "w") as file:
    json.dump(devices, file, indent=4)

session.close()
