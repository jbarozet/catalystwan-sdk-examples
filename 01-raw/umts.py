# =========================================================================
# Catalyst WAN SDK Examples: UMTS
#
# Steps:
# - umts_create
# - umts_start
# - umts_status
# - umts_download
# - umts_disable
# =========================================================================

import json
import os
import sys
from time import sleep
from typing import Optional
from uuid import UUID

import click

sys.path.insert(0, "..")
from utils.session import create_session

data_dir = "./payloads/umts/"


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK for UMTS"""
    pass


def create_folder():
    """
    Create payload folder
    """

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        print("\n~~~ Folder %s created!" % data_dir)
    else:
        print("\n~~~ Folder %s already exists" % data_dir)


def save_payload(result, type):
    """
    Save payload in backup folder
    """
    # Dictionary mapping types to filenames
    type_to_filename = {
        "create": "payload_umts_create.json",
        "stop": "payload_umts_stop.json",
        "start": "payload_umts_start.json",
        "status": "payload_umts_status.json",
        "download": "payload_umts_download.json",
        "disable": "payload_umts_disable.json",
    }

    # Get filename from dictionary, exit if type not found
    if type not in type_to_filename:
        exit(f"{type} type not supported")

    filename = "".join([data_dir, type_to_filename[type]])

    # Dump result to json
    print(f"\n~~~ Saving payload in file {filename}")
    with open(filename, "w") as file:
        json.dump(result, file, indent=4)


def save_session_id(session_id: UUID, filename: str = "umts_session.txt") -> None:
    """Save UMTS session ID (UUID) to a file"""
    with open(filename, "w") as f:
        f.write(str(session_id))


def get_saved_session_id(filename: str = "umts_session.txt") -> Optional[UUID]:
    """Retrieve UMTS session ID (UUID) from file"""
    try:
        with open(filename, "r") as f:
            session_id_str = f.read().strip()
            return UUID(session_id_str)
    except FileNotFoundError:
        print(f"Session ID file '{filename}' not found")
        return None
    except ValueError:
        print(f"Invalid UUID format in file '{filename}'")
        return None


@click.command()
def umts_create() -> str:
    print("\n\n~~~ CREATE SESSION")

    # Color: <color-name> or "remote-color-all"
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
    print(f"Created session ID: {umts_session_id}")
    save_payload(result, "create")

    # Save session ID to file
    save_session_id(umts_session_id)

    print(umts_session_id)
    return umts_session_id


@click.command()
def umts_start():
    print("\n\n~~~ START")

    session_id = get_saved_session_id()
    if session_id:
        # Use the session ID
        print(f"Retrieved session ID: {session_id}")

    url = f"/dataservice/stream/device/umts/start/{session_id}"
    try:
        result = session.get(url=url).json()
    except Exception as e:
        print(type(e))
        print(e)
        exit(1)

    save_payload(result, "start")


@click.command()
def umts_stop():
    print("\n\n~~~ STOP")

    session_id = get_saved_session_id()
    if session_id:
        # Use the session ID
        print(f"Retrieved session ID: {session_id}")

    url = f"/dataservice/stream/device/umts/stop/{session_id}"
    try:
        result = session.get(url=url).json()
    except Exception as e:
        print(type(e))
        print(e)
        exit(1)

    save_payload(result, "stop")


@click.command()
def umts_status() -> None:
    print("\n\n~~~ STATUS")

    session_id = get_saved_session_id()

    if session_id:
        # Use the session ID
        print(f"Retrieved session ID: {session_id}")

    url = f"/dataservice/stream/device/umts/status/{session_id}"

    try:
        result = session.get(url=url).json()
        save_payload(result, "status")
        if "status" not in result:
            print("Warning: 'status' key not found in response")
            return
        return
    except KeyError as e:
        print(f"KeyError: Missing key {e} in response")
        return
    except Exception as e:
        print(f"Error getting status: {type(e)} - {e}")
        return


@click.command()
def umts_download():
    print("\n\n~~~ DOWNLOAD")

    session_id = get_saved_session_id()
    if session_id:
        # Use the session ID
        print(f"Retrieved session ID: {session_id}")

    url = f"/dataservice/stream/device/umts/download/{session_id}"
    result = session.get(url=url).json()
    print(result)
    # result = session.get(url=url).json()["data"]
    # save_payload(result, "download")


@click.command()
def umts_disable():
    print("\n\n~~~ DISABLE")

    session_id = get_saved_session_id()
    if session_id:
        # Use the session ID
        print(f"Retrieved session ID: {session_id}")

    url = f"/dataservice/stream/device/umts/disable/{session_id}"
    result = session.get(url=url).json()
    save_payload(result, "disable")


# Create payload folder
create_folder()

# Run commands
cli.add_command(umts_create)
cli.add_command(umts_start)
cli.add_command(umts_stop)
cli.add_command(umts_status)
cli.add_command(umts_download)
cli.add_command(umts_disable)

if __name__ == "__main__":
    with create_session() as session:
        cli()
