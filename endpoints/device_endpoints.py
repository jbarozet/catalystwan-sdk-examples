import sys

sys.path.insert(0, "..")
from session import create_session

# Create session
session = create_session()


# ----------------------------------------------------------------------------------------------------
# All edge devices in inventory
# ----------------------------------------------------------------------------------------------------

device_inventory = session.endpoints.configuration_device_inventory

# Devices
devices = device_inventory.get_device_details("vedges")
print("\n~~~ Edge device inventory")
for item in devices:
    print(
        f" - uuid: {item.uuid} - device type: {item.device_type} - hostname: {item.host_name} - chassis number: {item.chasis_number}"
    )

# Controllers
controllers = device_inventory.get_device_details("controllers")
managers = controllers.filter(device_type="vmanage")
validators = controllers.filter(device_type="vbond")
controllers = controllers.filter(device_type="vsmart")

print("\n~~~ Controllers information")
for manager in managers:
    print(f" - Manager system IP: {manager.system_ip}")
for validator in validators:
    print(f" - Validator system IP: {validator.system_ip}")
for controller in controllers:
    print(f" - controller system IP: {controller.system_ip}")

# ----------------------------------------------------------------------------------------------------
# All edge devices used
# ----------------------------------------------------------------------------------------------------

print("\n~~~ All devices used")
devices = session.endpoints.monitoring_device_details.list_all_devices()
for item in devices:
    print(f" - uuid: {item.device_id} - hostname {item.host_name} - device_id: {item.device_id}")

session.close()
