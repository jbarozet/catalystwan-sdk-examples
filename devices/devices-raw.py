# Device APIs
#
# @author Jean-Marc Barozet <jbarozet@cisco.com>
#
# Using catalystwan-sdk package
# Layer1: core interface
#

import json
import os
import sys

import click
import tabulate

sys.path.insert(0, "..")
from utils.session import create_session


def save_json(payload: str, data: str):
    """Save json response payload to a file"""

    data_dir = "./payloads/"
    filename_data = "".join([data_dir, "payload_devices_data.json"])
    filename_payload = "".join([data_dir, "payload_devices_all.json"])

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


@click.group()
def cli():
    """Command line tool to showcase Catalyst WAN Python SDK"""
    pass


# --------------------------------------------------------------
# Configuration
# --------------------------------------------------------------


@click.command()
def system_routers():
    """Retrieve the list of all routers
    Example command: python devices-raw.py system_routers
    """

    with create_session() as session:
        # Configuration - Device Inventory
        url = "dataservice/system/device/vedges"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["UUID", "Model", "Solution", "Certificate"]
        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [
                item["uuid"],
                item["deviceModel"],
                item["solution"],
                item["vedgeCertificateState"],
            ]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
@click.option("--system_ip", help="System IP address of the device")
def system_router(system_ip):
    """Retrieve details about a device using its system IP address
    Example command: python devices-raw.py system_router --system_ip <system_ip>
    """

    with create_session() as session:
        # Configuration - Device Inventory
        url = "dataservice/system/device/vedges?deviceIP=%s" % (system_ip)
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
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
def system_controllers():
    """Retrieve the list of all controllers (Managers, Controllers, Validators)
    Example command: python devices-raw.py system_controllers
    """

    with create_session() as session:
        # Configuration - Device Inventory
        url = "dataservice/system/device/controllers"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["Hostname", "Type", "System IP", "Site ID", "UUID", "version"]
        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [
                item["host-name"],
                item["deviceType"],
                item["system-ip"],
                item["site-id"],
                item["uuid"],
                item["version"],
            ]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


# --------------------------------------------------------------
# Monitoring > Inventory
# url = "dataservice/device/vedgeinventory/summary" gives:
#   > url = "/dataservice/device/vedgeinventory/detail"
#   > url = "/dataservice/device/vedgeinventory/detail?status=authorized"
#   > url = "/dataservice/device/vedgeinventory/detail?status=deployed"
#   > url = "/dataservice/device/vedgeinventory/detail?status=staging"

# --------------------------------------------------------------


@click.command()
def inventory():
    """Retrieve the list of devices (wan edges)
    Example command: python devices-raw.py inventory
    """

    with create_session() as session:
        # Monitoring - Device Details
        url = "/dataservice/device/vedgeinventory/detail"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["Device Type", "System IP", "Chassis Number"]
        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [
                item["deviceType"],
                item["system-ip"],
                item["chasisNumber"],
            ]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def authorized():
    """Retrieve the list of devices (wan edges) that are authorized
    Example command: python devices-raw.py authorized
    """

    with create_session() as session:
        # Monitoring - Device Details
        url = "/dataservice/device/vedgeinventory/detail?status=authorized"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["Device Type", "System IP", "Chassis Number"]
        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [
                item["deviceType"],
                item["system-ip"],
                item["chasisNumber"],
            ]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def deployed():
    """Retrieve the list of devices (wan edges) that are deployed
    Example command: python devices-raw.py deployed
    """

    with create_session() as session:
        # Monitoring - Device Details
        url = "/dataservice/device/vedgeinventory/detail?status=deployed"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["Device Type", "System IP", "Chassis Number"]
        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [
                item["deviceType"],
                item["system-ip"],
                item["chasisNumber"],
            ]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def staging():
    """Retrieve the list of devices (wan edges) that are in staging mode
    Example command: python devices-raw.py staging
    """

    with create_session() as session:
        # Monitoring - Device Details
        url = "/dataservice/device/vedgeinventory/detail?status=staging"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["Device Type", "System IP", "Chassis Number"]
        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [
                item["deviceType"],
                item["system-ip"],
                item["chasisNumber"],
            ]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


# --------------------------------------------------------------
# Monitoring
# --------------------------------------------------------------


@click.command()
def devices():
    """Retrieve the list of all devices connected to the fabric
    Example command: python devices-raw.py connected
    """

    with create_session() as session:
        # Monitoring - Device Details
        url = "dataservice/device"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["Name", "UUID", "Type", "SystemI IP", "State"]
        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [item["host-name"], item["uuid"], item["personality"], item["system-ip"], item["state"]]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
@click.option("--system_ip", help="System IP address of the device")
def interface_status(system_ip):
    """Retrieve and return information about Interface status of network device
    Example command: python devices-raw.py interface-status --system_ip 10.0.0.1
    """

    with create_session() as session:
        # Monitoring - Device Details
        url = "/dataservice/device/interface/synced?deviceId={0}".format(system_ip)
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

        else:
            click.echo("Failed to get device list " + str(response.text))
            exit()

        headers = ["Interface Name", "IP address", "VPN ID", "Operational status"]
        table = list()

        for item in data:
            if item.get("ip-address") != "-":
                tr = [
                    item["ifname"],
                    item["ip-address"],
                    item["vpn-id"],
                    item["if-oper-status"],
                ]
                table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def config():
    """Retrieve device configuration using its uuid.
    Example command: python devices-raw.py config
    """

    device_uuid = input("Enter device UUID: ")
    # device_uuid = "C8K-3D1A8960-6E76-532C-DA93-50626FC5797E"

    with create_session() as session:
        url = "dataservice/template/config/running/%s" % (device_uuid)
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            running_config = payload["config"]
            save_json(payload, running_config)
        else:
            click.echo("Failed to get device configuration " + str(response.text))
            exit()

        print(running_config)


# ----------------------------------------------------------------------------------------------------
# Run commands
# ----------------------------------------------------------------------------------------------------

cli.add_command(system_routers)
cli.add_command(system_router)
cli.add_command(system_controllers)

cli.add_command(inventory)
cli.add_command(authorized)
cli.add_command(deployed)
cli.add_command(staging)

cli.add_command(devices)
cli.add_command(interface_status)
cli.add_command(config)

if __name__ == "__main__":
    cli()
