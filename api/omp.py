import sys

sys.path.insert(0, "..")
from catalystwan.dataclasses import Personality

from session import create_session

# Create Session
session = create_session()

# Get the list of devices
all_devices = session.api.devices.get()

edges = all_devices.filter(personality=Personality.EDGE)

for item in edges:
    print(f"~~~ {item.hostname} - {item.local_system_ip}")

# Get OMP peers
deviceid = input("Enter Device ID : ")
omp_peers = session.api.omp.get_omp_peers(deviceid)

for peer in omp_peers:
    print(f"vsmart: {peer.peerIp} - state: {peer.state} - SiteId: {peer.siteId} ")

session.close()
