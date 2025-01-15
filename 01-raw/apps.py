#! /usr/bin/env python3

import cmd
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
    """Command line tool for to collect application names."""
    pass


# ----------------------------------------------------------------------------------------------------
# app-list
# ----------------------------------------------------------------------------------------------------


@click.command()
def app_list():
    """Retrieve the list of Applications.
    Example command: python apps.py app-list
    """

    with create_session() as session:

        url = "dataservice/device/dpi/application-mapping"
        response = session.get(url)

        if response.status_code == 200:
            items = response.json()
            app_headers = ["App name", "Family", "ID"]
        else:
            click.echo("Failed to get list of Apps " + str(response.text))
            exit()

        table = list()
        # cli = cmd.Cmd()

        for item in items["data"]:
            tr = [item["name"], item["family"], item["appId"]]
            table.append(tr)

        click.echo(tabulate.tabulate(table, app_headers, tablefmt="fancy_grid"))


# ----------------------------------------------------------------------------------------------------
# app-list-2
# Display app-name and family in multi-column view
# ----------------------------------------------------------------------------------------------------


@click.command()
def app_list_2():
    """Retrieve the list of Applications.
    Example command: python apps.py app-list-2
    """

    with create_session() as session:

        url = "dataservice/device/dpi/application-mapping"
        response = session.get(url)

        if response.status_code == 200:
            items = response.json()
        else:
            click.echo("Failed to get list of Apps " + str(response.text))
            exit()

        table = list()
        cli = cmd.Cmd()

        for item in items["data"]:
            # print(item['name'])
            table.append(item["name"] + "(" + item["family"] + ")")

        click.echo(cli.columnize(table, displaywidth=120))


# ----------------------------------------------------------------------------------------------------
# app-list
# ----------------------------------------------------------------------------------------------------


@click.command()
def app_list_json():
    """Retrieve the list of Applications and save payload in json file
    Example command: python apps.py app-list-json
    """

    data_dir = "./payloads/"
    filename_data = "".join([data_dir, "payload_apps_data.json"])
    filename_payload = "".join([data_dir, "payload_apps_all.json"])

    with create_session() as session:

        url = "dataservice/device/dpi/application-mapping"
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            # Get rid of header section and only keep data
            data = payload["data"]
        else:
            click.echo("Failed to get list of Apps " + str(response.text))
            exit()

        # Create payload folder
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("\n~~~ Folder %s created!" % data_dir)
        else:
            print("\n~~~ Folder %s already exists" % data_dir)

        # Dump entire payload to file
        print(f"\n~~~ Saving payload in {filename_payload}")
        with open(filename_payload, "w") as file:
            json.dump(payload, file, indent=4)

        # Dump payload data (device list) to file
        print(f"\n~~~ Saving payload in {filename_data}")
        with open(filename_data, "w") as file:
            json.dump(data, file, indent=4)


# ----------------------------------------------------------------------------------------------------
# qosmos-list
# ----------------------------------------------------------------------------------------------------


@click.command()
def qosmos_list():
    """Retrieve the list of Qosmos Applications.
    Example command: python apps.py qosmos-list
    """

    with create_session() as session:

        url = "dataservice/device/dpi/qosmos-static/applications"
        response = session.get(url)

        if response.status_code == 200:
            items = response.json()
            app_headers = ["App name", "Family", "ID"]
        else:
            click.echo("Failed to get list of Apps " + str(response.text))
            exit()

        table = list()
        cli = cmd.Cmd()

        for item in items["data"]:
            tr = [item["name"], item["family"], item["appId"]]
            table.append(tr)

        click.echo(tabulate.tabulate(table, app_headers, tablefmt="fancy_grid"))


# ----------------------------------------------------------------------------------------------------
# Run commands
# ----------------------------------------------------------------------------------------------------

# Disable warning
requests.packages.urllib3.disable_warnings()

cli.add_command(app_list)
cli.add_command(app_list_2)
cli.add_command(qosmos_list)
cli.add_command(app_list_json)

if __name__ == "__main__":
    cli()
