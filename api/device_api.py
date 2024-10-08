import sys

sys.path.insert(0, "..")
from catalystwan.dataclasses import Personality

from utils.session import create_session

# Create session
session = create_session()


# Get the list of devices
devices = session.api.devices.get()
count = session.api.devices.count_devices(personality=Personality.EDGE)

print(f"count: {count}")

# Display the list of devices
print("\n~~~ All devices")
for dev in devices:
    print(f" - {dev.hostname} - Load: {dev.cpu_load} - Board serial: {dev.board_serial} - UUID: {dev.uuid}")
    # print(session.api.device_state.get_system_status(dev.id))

# Filter SD-WAN Controllers
vsmarts = devices.filter(personality=Personality.VSMART)

print("\n~~~ SD-WAN Controllers")

for item in vsmarts:
    print(
        f" - {item.hostname} - {item.local_system_ip} - Load: {item.cpu_load} - Board serial: {item.board_serial} - UUID: {item.uuid}"
    )

# Filter devices
edge_cpu = devices.filter(hostname="ciscotme-cloud-fabric-cedge-1").single_or_default().cpu_load
print("\n~~~ SD-WAN edge1")
print(f" - Edge CPU load: {edge_cpu}")

# Device Health
device_health = session.api.dashboard.get_devices_health_overview()
print("\n~~~ Device Health")
print(device_health)

# Tunnel Health
tunnel_health = session.api.dashboard.get_tunnel_health()
print("\n~~~ Tunnel Health")
print(tunnel_health)

session.close()

# ---END---
