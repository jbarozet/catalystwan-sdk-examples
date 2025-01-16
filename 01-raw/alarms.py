#! /usr/bin/env python3

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
    filename_data = "".join([data_dir, "payload_alarms_data.json"])
    filename_payload = "".join([data_dir, "payload_alarms_all.json"])

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
def list_all():
    """Get all alarms and save in a file"""

    # alarm_type = "omp-state-change"
    # alarm_type = "tloc_down"
    # alarm_type = "cpu-usage"
    # alarm_type = "system-reboot-issued",
    # alarm_type = "control-vbond-state-change",
    # alarm_type = "rootca-sync-failure"
    # alarm_type = "security-root-cert-chain-installed",
    # alarm_type = "disk-usage"
    # alarm_type = "sla-violation"

    url = "dataservice/alarms"

    start_time = "2025-01-01 08:00:00"
    end_time = "2025-01-16 13:00:00"

    payload = {
        "query": {
            "condition": "AND",
            "rules": [
                {
                    "field": "entry_time",
                    "operator": "between",
                    "type": "date",
                    "value": [start_time, end_time],
                },
            ],
        },
        "size": 10000,
    }

    with create_session() as session:

        response = session.post(url, data=json.dumps(payload))

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

        else:
            print("Failed to retrieve alarms\n")
            exit()


@click.command()
def list_cpu():
    """Get cpu usage alarms, display in a table and save in a file"""

    # alarm_type = "omp-state-change"
    # alarm_type = "tloc_down"
    # alarm_type = "cpu-usage"
    # alarm_type = "system-reboot-issued",
    # alarm_type = "control-vbond-state-change",
    # alarm_type = "rootca-sync-failure"
    # alarm_type = "security-root-cert-chain-installed",
    # alarm_type = "disk-usage"
    # alarm_type = "sla-violation"

    # site_id = input("Enter site_id: ")

    # url = "dataservice/alarms?site-id=" + str(site_id)
    url = "dataservice/alarms"

    start_time = "2025-01-01 08:00:00"
    end_time = "2025-01-16 13:00:00"
    alarm_type = "cpu-usage"

    print(start_time)
    print(end_time)

    payload = {
        "query": {
            "condition": "AND",
            "rules": [
                {
                    "field": "entry_time",
                    "operator": "between",
                    "type": "date",
                    "value": [start_time, end_time],
                },
                {
                    "field": "rulename",
                    "operator": "in",
                    "type": "string",
                    "value": [alarm_type],
                },
            ],
        },
        "size": 10000,
    }

    with create_session() as session:

        response = session.post(url, data=json.dumps(payload))

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

        else:
            print("Failed to retrieve Site Alarms\n")
            exit()

        headers = [
            "System-ip",
            "Host Name",
            "CPU Usage",
        ]

        table = list()

        for item in data:
            tr = [
                item["values"][0]["system-ip"],
                item["values"][0]["host-name"],
                item["values"][0]["cpu-status"],
            ]
            table.append(tr)
        try:
            click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
        except UnicodeEncodeError:
            click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


@click.command()
def list_tloc():
    """Get tloc_down alarms, display in a table and save in a file"""

    # alarm_type = "omp-state-change"
    # alarm_type = "tloc_down"
    # alarm_type = "cpu-usage"
    # alarm_type = "system-reboot-issued",
    # alarm_type = "control-vbond-state-change",
    # alarm_type = "rootca-sync-failure"
    # alarm_type = "security-root-cert-chain-installed",
    # alarm_type = "disk-usage"
    # alarm_type = "sla-violation"

    # site_id = input("Enter site_id: ")

    # url = "dataservice/alarms?site-id=" + str(site_id)
    url = "dataservice/alarms"

    start_time = "2025-01-01 08:00:00"
    end_time = "2025-01-16 13:00:00"
    alarm_type = "tloc_down"

    print(start_time)
    print(end_time)

    payload = {
        "query": {
            "condition": "AND",
            "rules": [
                {
                    "field": "entry_time",
                    "operator": "between",
                    "type": "date",
                    "value": [start_time, end_time],
                },
                {
                    "field": "rulename",
                    "operator": "in",
                    "type": "string",
                    "value": [alarm_type],
                },
            ],
        },
        "size": 10000,
    }

    with create_session() as session:

        response = session.post(url, data=json.dumps(payload))

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

        else:
            print("Failed to retrieve Site Alarms\n")
            exit()

        headers = ["System-ip", "Host Name", "Color", "site-id"]

        table = list()

        for item in data:
            tr = [
                item["values"][0]["system-ip"],
                item["values"][0]["host-name"],
                item["values"][0]["color"],
                item["values"][0]["site-id"],
            ]
            table.append(tr)
        try:
            click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
        except UnicodeEncodeError:
            click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


# ----------------------------------------------------------------------------------------------------
# Run commands
# ----------------------------------------------------------------------------------------------------

# Disable warning
requests.packages.urllib3.disable_warnings()

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="sdwan.log", level=logging.INFO)

cli.add_command(list_cpu)
cli.add_command(list_tloc)
cli.add_command(list_all)


if __name__ == "__main__":
    cli()
