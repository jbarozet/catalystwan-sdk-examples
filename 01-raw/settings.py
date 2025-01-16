import json
import logging
import os
import sys

import click
import requests
import tabulate

sys.path.insert(0, "..")
from utils.session import create_session


@click.group()
def cli():
    """Command line tool for to collect application names."""
    pass


def save_json(payload: str, data: str):
    """Save json response payload to a file"""

    data_dir = "./payloads/"
    filename_data = "".join([data_dir, "payload_settings_data.json"])
    filename_payload = "".join([data_dir, "payload_settings_all.json"])

    # Create payload folder
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        print("~~~ Folder %s created!" % data_dir)
    else:
        print("~~~ Folder %s already exists" % data_dir)

    # Dump entire payload to file
    print(f"~~~ Saving full payload in {filename_payload}")
    with open(filename_payload, "w") as file:
        json.dump(payload, file, indent=4)

    # Dump payload data (device list) to file
    print(f"~~~ Saving data payload in {filename_data}")
    with open(filename_data, "w") as file:
        json.dump(data, file, indent=4)


@click.command()
def get_vbond():
    """Get vbond name and save response payload in a file"""

    url = "dataservice/settings/configuration/device"

    with create_session() as session:

        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

        else:
            print("Failed to retrieve vbond\n")
            exit()

        for item in data:
            vbond = item["domainIp"]
            print(f"vbond: {vbond}")


@click.command()
def get_org():
    """Get organization name and save response payload in a file"""

    url = "dataservice/settings/configuration/organization"

    with create_session() as session:

        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

        else:
            print("Failed to retrieve organization\n")
            exit()

        for item in data:
            org = item["org"]
            print(f"organization: {org}")


# ----------------------------------------------------------------------------------------------------
# Run commands
# ----------------------------------------------------------------------------------------------------

# Disable warning
requests.packages.urllib3.disable_warnings()

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="sdwan.log", level=logging.INFO)

cli.add_command(get_vbond)
cli.add_command(get_org)


if __name__ == "__main__":
    cli()
