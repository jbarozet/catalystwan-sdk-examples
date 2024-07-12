import json
import os
import sys
from time import sleep

sys.path.insert(0, "..")
from utils.session import create_session


def save_payload(result):
    # Create payload folder
    path = "./payloads"
    if not os.path.exists(path):
        os.mkdir(path)
        print("\n~~~ Folder %s created!" % path)
    else:
        print("\n~~~ Folder %s already exists" % path)

    # Dump result to json
    filename = "payloads/payload_umts.json"
    print(f"\n~~~ Saving payload in file {filename}")
    with open(filename, "w") as file:
        json.dump(result, file, indent=4)


def umts_create() -> str:

    # UMTS session payload
    # Color:
    #   - private1
    # - remote-color-all
    session_payload = {
        "deviceUUID": "C8K-3D1A8960-6E76-532C-DA93-50626FC5797E",
        "localColor": "private1",
        "remoteColor": "private1",
        "remoteSystem": "10.0.0.2",
    }

    # Create stream
    url = "/dataservice/stream/device/umts"
    try:
        result = session.post(url=url, json=session_payload).json()
    except Exception as e:
        print(type(e))
        print(e)
        exit(1)

    umts_session_id = result["sessionId"]
    print("\n\n~~~ CREATE")
    print(result)
    print(umts_session_id)

    return umts_session_id


def umts_start(session_id: str):
    print("\n\n~~~ START")
    url = f"/dataservice/stream/device/umts/start/{session_id}"
    try:
        result = session.get(url=url).json()
    except Exception as e:
        print(type(e))
        print(e)
        exit(1)

    print(result)


def umts_status(session_id: str):
    print("\n\n~~~ STATUS")
    # session_id = "6994ea8a-2b2e-4798-8bd3-47da62ed69f8"
    url = f"/dataservice/stream/device/umts/status/{session_id}"
    result = session.get(url=url).json()
    print(result)


def umts_download(session_id: str):
    print("\n\n~~~ DOWNLOAD")
    url = f"/dataservice/stream/device/umts/download/{session_id}"
    result = session.get(url=url).json()["data"]
    print(result)


def umts_disable(session_id: str):
    print("\n\n~~~ DISABLE")
    url = f"/dataservice/stream/device/umts/disable/{session_id}"
    result = session.get(url=url).json()
    print(result)


if __name__ == "__main__":

    # Create SD-Manager session
    session = create_session()

    # Create UMTS session
    umts_session_id = umts_create()
    # umts_session_id = "6994ea8a-2b2e-4798-8bd3-47da62ed69f8"

    # Start UMTS session
    umts_start(umts_session_id)

    # Get UMTS session status
    umts_status(umts_session_id)

    sleep(20)

    # Download results
    umts_download(umts_session_id)

    # Close SD-Manager session
    session.close()
