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


# ----------------------------------------------------------------------------------------------------
# approute-fields
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


# ----------------------------------------------------------------------------------------------------
# approute-stats
# ----------------------------------------------------------------------------------------------------


@click.command()
def approute_stats():
    """Create Average Approute statistics for all tunnels between provided 2 routers for last 1 hour.
    Example command: python stats.py approute-stats
    """

    with create_session() as session:

        url = "dataservice/statistics/approute/aggregation"

        rtr1_systemip = input("Enter Router-1 System IP address : ")
        rtr2_systemip = input("Enter Router-2 System IP address : ")

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

        # response = requests.post(
        #     url=url, headers=header, data=json.dumps(payload), verify=False
        # )

        if response.status_code == 200:
            app_route_stats = response.json()["data"]
            app_route_stats_headers = [
                "Tunnel name",
                "vQoE score",
                "Latency",
                "Loss percentage",
                "Jitter",
            ]
            table = list()

            click.echo(
                "\nAverage App route statistics between %s and %s for last 1 hour\n"
                % (rtr1_systemip, rtr2_systemip)
            )

            for item in app_route_stats:
                tr = [
                    item["name"],
                    item["vqoe_score"],
                    item["latency"],
                    item["loss_percentage"],
                    item["jitter"],
                ]
                table.append(tr)
            try:
                click.echo(
                    tabulate.tabulate(
                        table, app_route_stats_headers, tablefmt="fancy_grid"
                    )
                )
            except UnicodeEncodeError:
                click.echo(
                    tabulate.tabulate(table, app_route_stats_headers, tablefmt="grid")
                )

        else:
            click.echo("Failed to retrieve app route statistics\n")


# Disable warning
requests.packages.urllib3.disable_warnings()

# ----------------------------------------------------------------------------------------------------
# Run commands
# ----------------------------------------------------------------------------------------------------

cli.add_command(approute_fields)
cli.add_command(approute_stats)


if __name__ == "__main__":
    cli()
