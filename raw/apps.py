import json
import os
import sys

import click
import tabulate

sys.path.insert(0, "..")
from utils.session import create_session


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def app_list():
    """Retrieve the list of Applications.
    Example command: ./apps.py app-list
    """
    # Using raw APIs
    response = session.get("/dataservice/device/dpi/application-mapping")
    payload = response.json()

    # Create payload folder
    path = "./payloads"
    if not os.path.exists(path):
        os.mkdir(path)
        print("\n~~~ Folder %s created!" % path)
    else:
        print("\n~~~ Folder %s already exists" % path)

    print("\n~~~ Saving payload in file payloads/payload_app_list.json")
    with open("payloads/payload_app_list.json", "w") as file:
        json.dump(payload, file, indent=4)

    # Format output
    table = list()
    app_headers = ["App name", "Family", "ID"]

    for item in payload["data"]:
        tr = [item["name"], item["family"], item["appId"]]
        table.append(tr)

    click.echo(tabulate.tabulate(table, app_headers, tablefmt="fancy_grid"))


@click.command()
def approute_fields():
    """Retrieve App route Aggregation API Query fields.
    Example command: ./apps.py approute-fields
    """
    # Using raw APIs
    response = session.get("/dataservice/statistics/approute/fields")
    payload = response.json()

    # Format output
    table = list()
    app_headers = ["Property", "Type"]

    for item in payload:
        tr = [item["property"], item["dataType"]]
        table.append(tr)

    click.echo(tabulate.tabulate(table, app_headers, tablefmt="fancy_grid"))


@click.command()
def approute_device():
    """Get Realtime Approute statistics for a specific tunnel for provided router and remote.
    Example command: ./monitor-app-route-stats.py approute-device
    """

    try:

        rtr1_systemip = input("Enter System IP address : ")
        rtr2_systemip = input("Enter Remote System IP address : ")
        color = input("Enter color : ")

        api_url = (
            "/dataservice/device/app-route/statistics?remote-system-ip=%s&local-color=%s&remote-color=%s&deviceId=%s"
            % (
                rtr2_systemip,
                color,
                color,
                rtr1_systemip,
            )
        )

        response = session.get(api_url)

        if response.status_code == 200:
            app_route_stats = response.json()["data"]
            app_route_stats_headers = [
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
            table = list()

            click.echo("\nRealtime App route statistics for %s to %s\n" % (rtr1_systemip, rtr2_systemip))
            for item in app_route_stats:
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
                click.echo(tabulate.tabulate(table, app_route_stats_headers, tablefmt="fancy_grid"))
            except UnicodeEncodeError:
                click.echo(tabulate.tabulate(table, app_route_stats_headers, tablefmt="grid"))

        else:
            click.echo("Failed to retrieve app route statistics\n")

    except Exception as e:
        print("Exception line number: {}".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


# Create vManage session
session = create_session()

# Run commands
cli.add_command(app_list)
cli.add_command(approute_fields)
cli.add_command(approute_device)

if __name__ == "__main__":
    cli()
