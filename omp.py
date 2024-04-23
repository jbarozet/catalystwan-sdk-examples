from session import create_session

# Create Session
session = create_session()

# Get OMP peers
# deviceid = "10.0.0.2"
deviceid = input("Enter Device ID : ")
omp_peers = session.api.omp.get_omp_peers(deviceid)

for peer in omp_peers:
    print(f"vsmart: {peer.peerIp} - state: {peer.state} - SiteId: {peer.siteId} ")
