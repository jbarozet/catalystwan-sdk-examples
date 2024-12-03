import json
import os
import sys

sys.path.insert(0, "..")
from utils.session import create_session

# Create payload folder
data_dir = "./payloads/"
filename_data = "".join([data_dir, "payload_devices_deployed_data.json"])
filename_payload = "".join([data_dir, "payload_devices_deployed_all.json"])
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
    print("\n~~~ Folder %s created!" % data_dir)
else:
    print("\n~~~ Folder %s already exists" % data_dir)


with create_session() as session:
    # Get list of devices
    # url_base = "dataservice/device/vedgeinventory/summary"
    url_base = "/dataservice/device/vedgeinventory/detail?status=deployed"
    payload = session.get(url_base).json()

    # Get rid of header section and only keep data
    devices = payload["data"]

    # Dump entire payload to file
    print(f"\n~~~ Saving payload in {filename_payload}")
    with open(filename_payload, "w") as file:
        json.dump(payload, file, indent=4)

    # Dump payload data (device list) to file
    print(f"\n~~~ Saving payload in {filename_data}")
    with open(filename_data, "w") as file:
        json.dump(devices, file, indent=4)
