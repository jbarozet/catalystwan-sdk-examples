from catalystwan.dataclasses import Personality

from session import create_session

# Create session
session = create_session()


# ----------------------------------------------------------------------------------------------------
# API - Display Device list
# ----------------------------------------------------------------------------------------------------

# Get the list of devices
devices = session.api.devices.get()

# Display the list of devices
print("\n--- List of devices")
for dev in devices:
    print(f"{dev.hostname} - Load: {dev.cpu_load} - Board serial: {dev.board_serial}")
    # print(session.api.device_state.get_system_status(dev.id))


# ----------------------------------------------------------------------------------------------------
# API - Filter device types
# ----------------------------------------------------------------------------------------------------

# Filter vmanage devices
vmanage = devices.filter(personality=Personality.VMANAGE).single_or_default()

# Display vManage information
print("\n--- vManage details")
print(f"Hostname: {vmanage.hostname}")
print(f"- System-IP: {vmanage.local_system_ip}")
print(f"- Load: {vmanage.cpu_load}")
print(f"- Board serial: {vmanage.board_serial}")

# ---END--
