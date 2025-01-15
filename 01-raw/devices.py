import json
import os
import sys

import click
import requests
import tabulate

sys.path.insert(0, "..")
from utils.session import create_session


# ----------------------------------------------------------------------------------------------------
# Click CLI
# ----------------------------------------------------------------------------------------------------


@click.group()
def cli():
    """Command line tool for to collect devices."""
    pass


@click.command()
def list_table():
    """Retrieve the list of devices (wan edges)
    Example command: python devices.py list-table
    """

    with create_session() as session:
        url_base = "dataservice/system/device/vedges"
        response = session.get(url_base)

    if response.status_code == 200:
        data = response.json()["data"]
        app_headers = ["UUID", "Model", "Certificate"]
    else:
        click.echo("Failed to get device list " + str(response.text))
        exit()

    table = list()

    for item in data:
        tr = [
            item["uuid"],
            item["deviceModel"],
            item["vedgeCertificateState"],
        ]
        table.append(tr)

    click.echo(tabulate.tabulate(table, app_headers, tablefmt="fancy_grid"))


@click.command()
def list_json():
    """Retrieve the list of devices (wan edges) and save json payload in file
    Example command: python devices.py list-json
    """

    # Create payload folder
    data_dir = "./payloads/"
    filename_data = "".join([data_dir, "payload_devices_data.json"])
    filename_payload = "".join([data_dir, "payload_devices_all.json"])

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        print("\n~~~ Folder %s created!" % data_dir)
    else:
        print("\n~~~ Folder %s already exists" % data_dir)

    with create_session() as session:
        url_base = "dataservice/system/device/vedges"
        payload = session.get(url_base).json()

        # Get rid of header section and only keep data
        devices = payload["data"]

        # Dump entire payload to file
        print(f"\n~~~ Saving payload in {filename_payload}")
        with open(filename_payload, "w") as file:
            json.dump(payload, file, indent=4)

        # Dump payload data (device list) to file
        print(f"\n~~~ Saving payload in {filename_data}")
        with open(filename_data, "w") as file:
            json.dump(devices, file, indent=4)


@click.command()
def list_deployed():
    """Retrieve the list of devices (wan edges) that are deployed
    Example command: python devices.py list-deployed-json
    """

    with create_session() as session:

        # Get list of devices
        # url_base = "dataservice/device/vedgeinventory/summary"
        url_base = "/dataservice/device/vedgeinventory/detail?status=deployed"
        response = session.get(url_base)

    if response.status_code == 200:
        data = response.json()["data"]
        app_headers = ["UUID", "host-name", "site-id", "system-ip"]
    else:
        click.echo("Failed to get device list " + str(response.text))
        exit()

    table = list()

    for item in data:
        tr = [
            item["chasisNumber"],
            item["host-name"],
            item["site-id"],
            item["system-ip"],
        ]
        table.append(tr)

    click.echo(tabulate.tabulate(table, app_headers, tablefmt="fancy_grid"))


@click.command()
def list_deployed_json():
    """Retrieve the list of devices (wan edges) that are deployed
    and save json payload in a file
    Example command: python devices.py list-deployed-json
    """

    with create_session() as session:

        # Create payload folder
        data_dir = "./payloads/"
        filename_data = "".join([data_dir, "payload_devices_deployed_data.json"])
        filename_payload = "".join([data_dir, "payload_devices_deployed_all.json"])

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("\n~~~ Folder %s created!" % data_dir)
        else:
            print("\n~~~ Folder %s already exists" % data_dir)

        # Get list of devices
        # url_base = "dataservice/device/vedgeinventory/summary"
        url_base = "/dataservice/device/vedgeinventory/detail?status=deployed"
        payload = session.get(url_base).json()

        # Get rid of header section and only keep data
        data = payload["data"]

        # Dump entire payload to file
        print(f"\n~~~ Saving payload in {filename_payload}")
        with open(filename_payload, "w") as file:
            json.dump(payload, file, indent=4)

        # Dump payload data (device list) to file
        print(f"\n~~~ Saving payload in {filename_data}")
        with open(filename_data, "w") as file:
            json.dump(data, file, indent=4)


@click.command()
def list_by_ip():
    """Retrieve details about a device using its system IP address
    Example command: python devices.py list-by-ip
    """

    systemip = input("Enter System IP address : ")

    with create_session() as session:
        url = "dataservice/system/device/vedges?deviceIP=%s" % (systemip)
        response = session.get(url)

        if response.status_code == 200:
            data = response.json()["data"]
        else:
            click.echo("Failed to get device " + str(response.text))
            exit()

        for item in data:
            tr = [
                item["configStatusMessage"],
                item["uuid"],
                item["deviceModel"],
                item["vedgeCertificateState"],
                item["deviceIP"],
                item["host-name"],
                item["version"],
                item["vmanageConnectionState"],
            ]

        print("\nDevice Information:")
        print("------------------")
        print("Device name: ", tr[5])
        print("Device IP: ", tr[4])
        print("UUID: ", tr[1])
        print("Device Model: ", tr[2])
        print("vManage Connection State: ", tr[7])
        print("Certificate state: ", tr[3])
        print("Version: ", tr[6])
        print("Config status: ", tr[0])


@click.command()
def config():
    """Retrieve device configuration using its uuid.
    Example command: python devices.py config
    """

    # device_uuid = input("Enter device UUID: ")
    device_uuid = "C8K-3D1A8960-6E76-532C-DA93-50626FC5797E"

    with create_session() as session:

        url = "dataservice//template/config/running/%s" % (device_uuid)
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            running_config = payload["config"]
        else:
            click.echo("Failed to get device configuration " + str(response.text))
            exit()
        print(running_config)


# ----------------------------------------------------------------------------------------------------
# Run commands
# ----------------------------------------------------------------------------------------------------

cli.add_command(list_table)
cli.add_command(list_json)
cli.add_command(list_by_ip)
cli.add_command(list_deployed)
cli.add_command(list_deployed_json)
cli.add_command(config)

if __name__ == "__main__":
    cli()
