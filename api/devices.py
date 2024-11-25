import sys

sys.path.insert(0, "..")
from catalystwan.dataclasses import Personality

from utils.session import create_session

# Create session
session = create_session()


# Get the list of devices
devices = session.api.devices.get()
count = session.api.devices.count_devices(personality=Personality.EDGE)
print(f"\nNumber of WAN Edge devices in the fabric: {count}")
# Display the list of devices
print("\n~~~ All devices")
for dev in devices:
    print(f" - {dev.hostname} - Board serial: {dev.board_serial} - UUID: {dev.uuid}")
    # print(session.api.device_state.get_system_status(dev.id))

# Filter SD-WAN Controllers
vsmarts = devices.filter(personality=Personality.VSMART)

print("\n~~~ SD-WAN Controllers")

for item in vsmarts:
    print(f" - {item.hostname} - {item.local_system_ip} - Board serial: {item.board_serial} - UUID: {item.uuid}")

# Filter devices
edge_cpu = devices.filter(hostname="site1-cedge01").single_or_default().cpu_load
print("\n~~~ SD-WAN edge1")
print(f" - Edge CPU load: {edge_cpu}")

# Device Health
device_health = session.api.dashboard.get_devices_health_overview()
print("\n~~~ Device Health")
print(f"Good: {device_health.single_or_default().good}")
print(f"Fair: {device_health.single_or_default().fair}")
print(f"Poor: {device_health.single_or_default().poor}")

# Tunnel Health
tunnel_health = session.api.dashboard.get_tunnel_health()
print("\n~~~ Tunnel Health")
for item in tunnel_health:
    print(f"{item.name} - score: {item.vqoe_score}")

session.close()

# ---END---
