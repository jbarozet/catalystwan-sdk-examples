import sys
import tabulate

sys.path.insert(0, "..")
from catalystwan.dataclasses import Personality

from utils.session import create_session

# Create Session
session = create_session()

# Get the list of devices
all_devices = session.api.devices.get()

edges = all_devices.filter(personality=Personality.EDGE)

table = list()
headers = ["Device Name", "System IP", "Reachable"]

for item in edges:
    tr = [item.hostname, item.local_system_ip, item.is_reachable]
    table.append(tr)

print(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


# Get OMP peers
deviceid = input("\nEnter Device ID : ")
omp_peers = session.api.omp.get_omp_peers(deviceid)

for peer in omp_peers:
    print(f"vsmart: {peer.peerIp} - state: {peer.state} - SiteId: {peer.siteId} ")

session.close()
