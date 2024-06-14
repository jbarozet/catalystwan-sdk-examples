import os

import urllib3
from catalystwan.session import ManagerSession, create_manager_session

# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Create vManage session
def create_session() -> ManagerSession:
    """Create vManage session"""

    url = os.environ.get("vmanage_host")
    user = os.environ.get("vmanage_user")
    password = os.environ.get("vmanage_password")

    if url is None or user is None or password is None:
        print("For Windows Workstation, vManage details must be set via environment variables using below commands")
        print("set vmanage_host=10.10.1.1")
        print("set vmanage_port=8443")
        print("set vmanage_user=admin")
        print("set vmanage_password=admin")
        print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
        print("export vmanage_host=10.10.1.1")
        print("export vmanage_port=8443")
        print("export vmanage_user=admin")
        print("export vmanage_password=admin")
        exit()

    session = create_manager_session(url=url, username=user, password=password)

    print("~~~  Session Information")
    print(f" - vManage: {session.url}")
    print(f" - Version: {session.about().version}")
    print(f" - API Version: {session.api_version}")
    print(f" - Application Version: {session.about().application_version}")

    return session
