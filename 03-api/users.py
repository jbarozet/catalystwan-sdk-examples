# Create/List/Delete user
# To enable log:
# export catalystwan_devel=1
# That will create a catalystwan.log file

import sys
import tabulate
import click

from catalystwan.api.administration import User
from catalystwan.session import ManagerSession

sys.path.insert(0, "..")
from utils.session import create_session


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def ls():

    with create_session() as session:

        users = session.api.users.get()

        table = list()
        headers = ["Username", "Group"]

        for user in users:
            tr = [user.username, user.group, user.resource_group]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def add():

    username = input("\nEnter username to add: ")
    password = "test!@#"
    group = ["netadmin"]
    description = "Test"

    with create_session() as session:

        new_user = User(
            username=username, password=password, group=group, description=description
        )
        session.api.users.create(new_user)


@click.command()
def delete():

    username = input("\nEnter username to add: ")

    with create_session() as session:

        session.api.users.delete(username=username)


if __name__ == "__main__":

    # Add commands
    cli.add_command(ls)
    cli.add_command(add)
    cli.add_command(delete)

    # Run commands
    cli()
