import json
import os
import sys
import tabulate
import click

sys.path.insert(0, "..")
from utils.session import create_session


def save_json(payload: str, data: str):
    """Save json response payload to a file"""

    data_dir = "./payloads/"
    filename_data = "".join([data_dir, "payload_users_data.json"])
    filename_payload = "".join([data_dir, "payload_users_all.json"])

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
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def ls():
    """List all user"""

    with create_session() as session:
        url_base = "/dataservice/admin/user"
        response = session.get(url=url_base)

        if response.status_code == 200:
            payload = response.json()
            data = response.json()["data"]
            save_json(payload, data)
            headers = ["Username", "Group"]
        else:
            click.echo("Failed to get user list " + str(response.text))
            exit()

        table = list()

        for item in data:
            tr = [
                item["userName"],
                item["group"],
            ]
            table.append(tr)

        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def add():
    """Add a user"""

    print("\n~~~ Adding user")
    username = input("\nEnter username to add: ")

    user_payload = {
        "userName": username,
        "description": "Demo User",
        "locale": "en_US",
        "group": ["netadmin"],
        "password": "my_super_password",
        "resGroupName": "global",
    }

    with create_session() as session:
        url_base = "/dataservice/admin/user"
        response = session.post(url=url_base, json=user_payload)

        if response.status_code == 200:
            click.echo("User successfully created ")

        else:
            click.echo("Failed to add user " + str(response.text))
            exit()


@click.command()
def delete():
    """Delete a user"""

    print("\n~~~ Deleting user")
    username = input("\nEnter username to delete: ")

    with create_session() as session:
        url = f"/dataservice/admin/user/{username}"
        response = session.delete(url=url)

        if response.status_code == 200:
            click.echo("User successfully deleted ")

        else:
            click.echo("Failed to delete user " + str(response.text))
            exit()


if __name__ == "__main__":

    # Add commands
    cli.add_command(ls)
    cli.add_command(add)
    cli.add_command(delete)

    # Run commands
    cli()
