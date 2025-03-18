#! /usr/bin/env python3


import json
import logging
import os
import sys

import click
import tabulate
import urllib3

sys.path.insert(0, "..")
from datetime import datetime

from utils.session import create_session


@click.group()
def cli():
    """Command line tool for to collect application names."""
    pass


def convert_unix_timestamp(timestamp: str) -> str:
    """Convert unix timestamp to datetime object"""

    dt = datetime.fromtimestamp(int(timestamp) / 1000)
    human_readable_date = dt.strftime("%A, %B %d, %Y, %I:%M:%S.%f %p")
    return human_readable_date
    # return datetime.fromtimestamp(int(timestamp))


def save_json(filename: str, payload: str, data: str):
    """Save json response payload to a file"""

    data_dir = "./payloads/"
    filename_data = "".join([data_dir, "payload_alarms_", filename, "_data.json"])
    filename_payload = "".join([data_dir, "payload_alarms_", filename, "_field_data.json"])

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
    print(f"~~~ Saving data payload in {filename_data}\n")
    with open(filename_data, "w") as file:
        json.dump(data, file, indent=4)


@click.command()
def list_alarms():
    """Mapping: alarm to severity"""

    url = "dataservice/alarms"
    name = "alarmsseverity"

    with create_session() as session:
        response = session.get(url)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(name, payload, data)
        else:
            click.echo("Failed to retrieve alarms " + str(response.text))
            exit()

        headers = ["UUID", "Model", "Certificate"]

        table = list()

        for item in data:
            tr = [
                item["type"],
                item["severity"],
                item["devices"][0]["system-ip"],
            ]
            table.append(tr)
        try:
            click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
        except UnicodeEncodeError:
            click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


@click.command()
def list_all():
    """Get all alarms and save in a file"""

    url = "dataservice/alarms"
    name = "all"

    start_time = "2025-01-01 08:00:00"
    end_time = "2025-01-17 20:00:00"

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
            save_json(name, payload, data)

        else:
            print("Failed to retrieve alarms\n")
            exit()

        headers = [
            "Date",
            "Type",
            "Severity",
            "System-ip",
        ]

        table = list()

        for item in data:
            human_readable_date = convert_unix_timestamp(item["entry_time"])

            tr = [
                human_readable_date,
                item["type"],
                item["severity"],
                item["devices"][0]["system-ip"],
            ]
            table.append(tr)
        try:
            click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
        except UnicodeEncodeError:
            click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


@click.command()
def list_cpu():
    """Get cpu usage alarms, display in a table and save in a file"""

    url = "dataservice/alarms"
    name = "cpu"

    start_time = "2025-01-01 08:00:00"
    end_time = "2025-03-16 13:00:00"
    # alarm_type = "cpu-usage"  # query "field": "rulename"
    alarm_name = "CPU_Usage"  # query "field": "rule_name_display"

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
                    "field": "rule_name_display",
                    "operator": "in",
                    "type": "string",
                    "value": [alarm_name],
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
            save_json(name, payload, data)

        else:
            print("Failed to retrieve alarms\n")
            exit()

        headers = [
            "Date",
            "System-ip",
            "Host Name",
            "CPU Usage",
        ]

        table = list()

        for item in data:
            human_readable_date = convert_unix_timestamp(item["entry_time"])

            tr = [
                human_readable_date,
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
def list_mem():
    """Get memory usage alarms, display in a table and save in a file"""

    url = "dataservice/alarms"
    name = "memory"

    start_time = "2025-01-01 08:00:00"
    end_time = "2025-03-16 13:00:00"
    alarm_name = "Memory_Usage"

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
                    "field": "rule_name_display",
                    "operator": "in",
                    "type": "string",
                    "value": [alarm_name],
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
            save_json(name, payload, data)

        else:
            print("Failed to retrieve alarms\n")
            exit()


@click.command()
def list_tloc():
    """Get tloc_down alarms, display in a table and save in a file"""

    url = "dataservice/alarms"
    name = "tloc"

    start_time = "2025-01-01 08:00:00"
    end_time = "2025-01-16 13:00:00"
    alarm_type = "tloc_down"

    print(start_time)
    print(end_time)

    query_payload = {
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
        response = session.post(url, data=json.dumps(query_payload))

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(name, payload, data)

        else:
            print("Failed to retrieve alarms\n")
            exit()

        headers = ["Date", "System-ip", "Host Name", "Color", "site-id", "type", "severity"]

        table = list()

        for item in data:
            human_readable_date = convert_unix_timestamp(item["entry_time"])

            tr = [
                human_readable_date,
                item["values"][0]["system-ip"],
                item["values"][0]["host-name"],
                item["values"][0]["color"],
                item["values"][0]["site-id"],
                item["type"],
                item["severity"],
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
# requests.packages.urllib3.disable_warnings()
urllib3.disable_warnings()

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="sdwan.log", level=logging.INFO)

cli.add_command(list_cpu)
cli.add_command(list_tloc)
cli.add_command(list_all)
cli.add_command(list_mem)


if __name__ == "__main__":
    cli()
