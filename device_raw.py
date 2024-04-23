import json
import os

import urllib3

# from vmngclient.dataclasses import Personality
from catalystwan.session import create_manager_session

# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CREATE SESSION

url = os.environ.get("vmanage_host")
user = os.environ.get("vmanage_user")
password = os.environ.get("vmanage_password")

session = create_manager_session(url=url, username=user, password=password)
print(session.about())

# RAW APIs
response = session.get("/dataservice/device")
payload = response.json()
# print(payload)

payloadJSON = json.dumps(payload, indent=4)
print(payloadJSON)
