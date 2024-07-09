import os

import urllib3
from catalystwan.session import ManagerSession, create_manager_session
from dotenv import load_dotenv

# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Create vManage session
def create_session() -> ManagerSession:
    """Create vManage session"""

    load_dotenv()

    url = os.getenv("vmanage_host")
    user = os.getenv("vmanage_user")
    password = os.getenv("vmanage_password")

    if url is None or user is None or password is None:
        print("Define vManage parameters in .env file")
        exit()

    print(f"SD-WAN Manager: {url} - user: {user}")

    session = create_manager_session(url=url, username=user, password=password)

    print("~~~  Session Information")
    print(f" - vManage: {session.url}")
    print(f" - Version: {session.about().version}")
    print(f" - API Version: {session.api_version}")
    print(f" - Application Version: {session.about().application_version}")

    return session
