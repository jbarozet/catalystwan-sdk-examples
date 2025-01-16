#! /usr/bin/env python3

import cmd
import json
import logging
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


def save_json(payload: str, data: str):
    """Save json response payload to a file"""

    data_dir = "./payloads/"
    filename_data = "".join([data_dir, "payload_stats_data.json"])
    filename_payload = "".join([data_dir, "payload_stats_all.json"])

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


# ----------------------------------------------------------------------------------------------------
# approute-fields
# ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------
# STATISTCS
# ----------------------------------------------------------------------------------------------------


@click.command()
def device():
    """Get device statistics for last 1 hour."""

    rtr1_systemip = input("Enter Router-1 System IP address : ")

    with create_session() as session:

        url = "dataservice/statistics/device/"

        payload = {
            "query": {
                "condition": "AND",
                "rules": [
                    {
                        "value": ["1"],
                        "field": "entry_time",
                        "type": "date",
                        "operator": "last_n_hours",
                    },
                    {
                        "value": [rtr1_systemip],
                        "field": "vdevice_name",
                        "type": "string",
                        "operator": "in",
                    },
                ],
            },
        }

        response = session.post(url, data=json.dumps(payload))

        if response.status_code == 200:

            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

            headers = [
                "Device Name",
                "Device Model",
                "Local System IP",
                "Remote System IP",
                "state",
                "Local Color",
                "Remote Color",
                "VQoE Score",
                "Latency",
                "Loss Percentage",
                "Jitter",
            ]
            table = list()

            click.echo(
                "\nApp route statistics for %s for last 1 hour\n" % (rtr1_systemip)
            )

            for item in data:
                tr = [
                    item["host_name"],
                    item["device_model"],
                    item["local_system_ip"],
                    item["remote_system_ip"],
                    item["state"],
                    item["local_color"],
                    item["remote_color"],
                    item["vqoe_score"],
                    item["latency"],
                    item["loss_percentage"],
                    item["jitter"],
                ]
                table.append(tr)
            try:
                click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
            except UnicodeEncodeError:
                click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

        else:
            click.echo("Failed to retrieve app route statistics\n")


@click.command()
def approute():
    """Get approute statistics for all tunnels for a router for last 1 hour.
    Example command: python stats.py approute
    """

    rtr_systemip = input("Enter Router-1 System IP address : ")

    with create_session() as session:

        url = "dataservice/statistics/approute/"

        payload = {
            "query": {
                "condition": "AND",
                "rules": [
                    {
                        "value": ["2"],
                        "field": "entry_time",
                        "type": "date",
                        "operator": "last_n_hours",
                    },
                    {
                        "value": [rtr_systemip],
                        "field": "vdevice_name",
                        "type": "string",
                        "operator": "in",
                    },
                    {
                        "value": ["mpls", "biz-internet"],
                        "field": "local_color",
                        "type": "string",
                        "operator": "in",
                    },
                ],
            },
        }

        response = session.post(url, data=json.dumps(payload))

        if response.status_code == 200:

            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

            headers = [
                "Device Name",
                "Local System ip",
                "Remote System ip",
                "Local Color",
                "Remote Color",
                "Latency",
                "Loss Percentage",
                "Jitter",
            ]
            table = list()

            click.echo(
                "\nApp route statistics for %s for last 1 hour\n" % (rtr_systemip)
            )

            for item in data:
                tr = [
                    item["vdevice_name"],
                    item["local_system_ip"],
                    item["remote_system_ip"],
                    item["local_color"],
                    item["remote_color"],
                    item["latency"],
                    item["loss_percentage"],
                    item["jitter"],
                ]
                table.append(tr)
            try:
                click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
            except UnicodeEncodeError:
                click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

        else:
            click.echo("Failed to retrieve app route statistics\n")


@click.command()
def dpi():
    """Get dpi statistics for last 1 hour.
    Example command: python stats.py dpi
    """

    rtr_systemip = input("Enter Router-1 System IP address : ")
    hours = 1

    with create_session() as session:

        url = "dataservice/statistics/dpi/"

        payload = {
            "query": {
                "condition": "AND",
                "rules": [
                    {
                        "value": [hours],
                        "field": "entry_time",
                        "type": "date",
                        "operator": "last_n_hours",
                    },
                    {
                        "value": [rtr_systemip],
                        "field": "vdevice_name",
                        "type": "string",
                        "operator": "in",
                    },
                ],
            },
        }

        response = session.post(url, data=json.dumps(payload))

        if response.status_code == 200:

            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)

            headers = [
                "VPN",
                "Src IP",
                "Dest IP",
                "Src port",
                "Dest Port",
                "Application",
            ]
            table = list()

            click.echo(
                "\nDPI statistics for %s for last %s hour\n" % (rtr_systemip, hours)
            )

            for item in data:
                tr = [
                    item["vpn_id"],
                    item["source_ip"],
                    item["dest_ip"],
                    item["source_port"],
                    item["dest_port"],
                    item["application"],
                ]
                table.append(tr)
            try:
                click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
            except UnicodeEncodeError:
                click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

        else:
            click.echo("Failed to retrieve app route statistics\n")


# ----------------------------------------------------------------------------------------------------
# STATISTCS - AGGREGATED
# ----------------------------------------------------------------------------------------------------


@click.command()
def approute_fields():
    """Retrieve App route Aggregation API Query fields.
    Example command: python stats.py approute-fields
    """

    with create_session() as session:

        url = "dataservice/statistics/approute/fields"
        payload = session.get(url).json()

        tags = list()
        cli = cmd.Cmd()

        for item in payload:
            tags.append(item["property"] + "(" + item["dataType"] + ")")

        click.echo(cli.columnize(tags, displaywidth=120))


@click.command()
def approute_agg():
    """Get average approute statistics for all tunnels between provided 2 routers for last 1 hour.
    Example command: python stats.py approute-agg
    """

    rtr1_systemip = input("Enter Router-1 System IP address : ")
    rtr2_systemip = input("Enter Router-2 System IP address : ")
    hours = 1

    with create_session() as session:

        url = "dataservice/statistics/approute/aggregation"

        payload = {
            "query": {
                "condition": "AND",
                "rules": [
                    {
                        "value": [hours],
                        "field": "entry_time",
                        "type": "date",
                        "operator": "last_n_hours",
                    },
                    {
                        "value": [rtr1_systemip],
                        "field": "local_system_ip",
                        "type": "string",
                        "operator": "in",
                    },
                    {
                        "value": [rtr2_systemip],
                        "field": "remote_system_ip",
                        "type": "string",
                        "operator": "in",
                    },
                ],
            },
            "aggregation": {
                "field": [{"property": "name", "sequence": 1, "size": 6000}],
                "metrics": [
                    {"property": "loss_percentage", "type": "avg"},
                    {"property": "vqoe_score", "type": "avg"},
                    {"property": "latency", "type": "avg"},
                    {"property": "jitter", "type": "avg"},
                ],
            },
        }

        response = session.post(url, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()["data"]
            headers = [
                "Tunnel name",
                "vQoE score",
                "Latency",
                "Loss percentage",
                "Jitter",
            ]
            table = list()

            click.echo(
                "\nAverage App route statistics between %s and %s for last %s hour\n"
                % (rtr1_systemip, rtr2_systemip, hours)
            )

            for item in data:
                tr = [
                    item["name"],
                    item["vqoe_score"],
                    item["latency"],
                    item["loss_percentage"],
                    item["jitter"],
                ]
                table.append(tr)
            try:
                click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
            except UnicodeEncodeError:
                click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

        else:
            click.echo("Failed to retrieve app route statistics\n")


# ----------------------------------------------------------------------------------------------------
# REALTIME
# stats collected from device
# ----------------------------------------------------------------------------------------------------


@click.command()
def approute_device():
    """Get REALTIME Approute statistics for a specific tunnel for provided router and remote.
    Example command: python stats approute-device
    """

    rtr1_systemip = input("Enter System IP address : ")
    rtr2_systemip = input("Enter Remote System IP address : ")
    color = input("Enter color : ")

    url = (
        "dataservice/device/app-route/statistics?remote-system-ip=%s&local-color=%s&remote-color=%s&deviceId=%s"
        % (
            rtr2_systemip,
            color,
            color,
            rtr1_systemip,
        )
    )

    with create_session() as session:

        response = session.get(url)

        if response.status_code == 200:
            data = response.json()["data"]
            headers = [
                "vdevice-host-name",
                "remote-system-ip",
                "Index",
                "Mean Latency",
                "Mean Jitter",
                "Mean Loss",
                "average-latency",
                "average-jitter",
                "loss",
            ]

        else:
            click.echo("Failed to retrieve app route statistics\n")
            exit()

        table = list()

        click.echo(
            "\nRealtime App route statistics for %s to %s\n"
            % (rtr1_systemip, rtr2_systemip)
        )
        for item in data:
            tr = [
                item["vdevice-host-name"],
                item["remote-system-ip"],
                item["index"],
                item["mean-latency"],
                item["mean-jitter"],
                item["mean-loss"],
                item["average-latency"],
                item["average-jitter"],
                item["loss"],
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

cli.add_command(approute_fields)
cli.add_command(device)
cli.add_command(approute)
cli.add_command(dpi)
cli.add_command(approute_agg)
cli.add_command(approute_device)


if __name__ == "__main__":
    cli()
