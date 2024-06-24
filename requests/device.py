#! /usr/bin/env python

# import cmd
import json
import logging
import os

import click
import tabulate
from settings import Settings
from vmanage import Authentication

import requests

# import sys


# ----------------------------------------------------------------------------------------------------
# Click CLI
# ----------------------------------------------------------------------------------------------------


@click.group()
def cli():
    """Command line tool for to collect application names)."""
    pass


# ----------------------------------------------------------------------------------------------------
# Get Device by IP
# /system/device/{type}?deviceIP={ip_address}
# ----------------------------------------------------------------------------------------------------


@click.command()
def get_devices():

    type = "vedges"

    api_url = "/system/device/%s" % (type)
    url = base_url + api_url

    response = requests.get(url=url, headers=header, verify=False)
    if response.status_code == 200:
        items = response.json()["data"]
        app_headers = ["UUID", "DeviceIP", "Model", "Certificate"]
    else:
        click.echo("Failed to get device list " + str(response.text))
        exit()

    content = response.json()

    # Print json output
    # content_json = json.dumps(content, indent=4)
    # print(content_json)

    # Write json output to file
    with open("devices.json", "w") as file:
        json.dump(content, file, indent=4)

    table = list()

    for item in items:
        tr = [item["uuid"], item["deviceIP"], item["deviceModel"], item["vedgeCertificateState"]]
        table.append(tr)

    click.echo(tabulate.tabulate(table, app_headers, tablefmt="fancy_grid"))


# ----------------------------------------------------------------------------------------------------
# Get Device by IP
# /system/device/{type}?deviceIP={ip_address}
# ----------------------------------------------------------------------------------------------------


@click.command()
def get_device_by_ip():

    type = "vedges"
    systemip = input("Enter System IP address : ")

    api_url = "/system/device/%s?deviceIP=%s" % (type, systemip)
    url = base_url + api_url

    response = requests.get(url=url, headers=header, verify=False)
    if response.status_code == 200:
        items = response.json()["data"]
    else:
        click.echo("Failed to get device " + str(response.text))
        exit()

    for item in items:
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


# ----------------------------------------------------------------------------------------------------
# Get Device Configuration
# dataservice/template/config/running/C8K-F46CCF9F-4D62-EEA5-293F-DDA4875BE30D
# ----------------------------------------------------------------------------------------------------


@click.command()
def get_device_config():
    api_url = "/template/config/running/C8K-F46CCF9F-4D62-EEA5-293F-DDA4875BE30D"
    url = base_url + api_url

    response = requests.get(url=url, headers=header, verify=False)
    if response.status_code == 200:
        items = response.json()
        running_config = items["config"]
    else:
        click.echo("Failed to get device configuration " + str(response.text))
        exit()
    print(running_config)


# ----------------------------------------------------------------------------------------------------
# Get Settings
# ----------------------------------------------------------------------------------------------------


@click.command()
def get_org():
    settings = Settings(header, vmanage_host, vmanage_port)
    org = settings.get_vmanage_org()
    print(org)


@click.command()
def get_vbond():
    settings = Settings(header, vmanage_host, vmanage_port)
    vbond = settings.get_vbond()
    print(vbond)


# Disable warning
requests.packages.urllib3.disable_warnings()

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="sdwan.log", level=logging.INFO)

# Get Parameters
vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
vmanage_username = os.environ.get("vmanage_user")
vmanage_password = os.environ.get("vmanage_password")

if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=198.18.1.10")
    print("set vmanage_port=8443")
    print("set vmanage_user=admin")
    print("set vmanage_password=admin")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=198.18.1.10")
    print("export vmanage_port=8443")
    print("export vmanage_user=admin")
    print("export vmanage_password=admin")
    exit()

# Authenticate with vManage
vmanage = Authentication(vmanage_host, vmanage_port, vmanage_username, vmanage_password)
jsessionid = vmanage.login()
if jsessionid:
    logger.info(f"Login successful, JSESSIONID: {jsessionid}")
    token = vmanage.get_token()
    if token:
        logger.info(f"Token retrieved: {token}")
    else:
        logger.error("Failed to retrieve token")
else:
    logger.error("Login failed")

if token is not None:
    header = {"Content-Type": "application/json", "Cookie": jsessionid, "X-XSRF-TOKEN": token}
else:
    header = {"Content-Type": "application/json", "Cookie": jsessionid}

base_url = "https://%s:%s/dataservice" % (vmanage_host, vmanage_port)


# ----------------------------------------------------------------------------------------------------
# Run commands
# ----------------------------------------------------------------------------------------------------

cli.add_command(get_org)
cli.add_command(get_vbond)
cli.add_command(get_device_config)
cli.add_command(get_device_by_ip)
cli.add_command(get_devices)

if __name__ == "__main__":
    cli()
