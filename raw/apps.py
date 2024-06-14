import sys

import click
import tabulate

sys.path.insert(0, "..")

from session import create_session


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


# Create vManage session
session = create_session()

# Run commands
cli.add_command(app_list)
cli.add_command(approute_fields)

if __name__ == "__main__":
    cli()
