import sys

sys.path.insert(0, "..")
from catalystwan.utils.personality import Personality

from utils.session import create_session

# Create session
session = create_session()

devices = session.api.devices.get()

for p in Personality:
    pds = devices.filter(personality=p)
    session.api.software.activate(pds, "20.9.1-377")

session.close()
