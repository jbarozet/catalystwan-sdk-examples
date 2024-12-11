import os
import sys

import urllib3
from catalystwan.session import ManagerSession, create_manager_session
from dotenv import load_dotenv

# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_session() -> ManagerSession:
    """
    Create vManage session with error handling.

    Returns:
        ManagerSession: Authenticated session to vManage

    Raises:
        SystemExit: If environment variables are missing or connection fails
    """
    try:
        load_dotenv()

        url = os.getenv("vmanage_host")
        user = os.getenv("vmanage_user")
        password = os.getenv("vmanage_password")

        if not all([url, user, password]):
            raise ValueError("Missing required vManage parameters in .env file")

        print(f"\n- Connecting to SD-WAN Manager: {url} - user: {user} ...")

        session = create_manager_session(url=str(url), username=str(user), password=str(password))

        # Validate connection by getting version info
        about = session.about()

        print(f"- vManage: {session.base_url}")
        print(f"- Version: {about.version}")
        print(f"- API Version: {session.api_version}")
        print(f"- Application Version: {about.application_version}")
        print("")

        return session

    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to connect to vManage: {str(e)}")
        sys.exit(1)
