from catalystwan.dataclasses import Personality

from session import create_session

# Create session
session = create_session()


# ----------------------------------------------------------------------------------------------------
# Endpoints - Devices
# ----------------------------------------------------------------------------------------------------

device_inventory = session.endpoints.configuration_device_inventory
control_components = device_inventory.get_device_details("controllers")
managers = control_components.filter(device_type="vmanage")
validators = control_components.filter(device_type="vbond")
controllers = control_components.filter(device_type="vsmart")

print("\n--- Controllers information")
for manager in managers:
    print(f"Manager system IP: {manager.system_ip}")
for validator in validators:
    print(f"Validator system IP: {validator.system_ip}")
for controller in controllers:
    print(f"controller system IP: {controller.system_ip}")
