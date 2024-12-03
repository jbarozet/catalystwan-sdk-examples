import json
import os
import sys

import click

sys.path.insert(0, "..")
from utils.session import create_session


def save_payload(result):
    # Create payload folder
    path = "./payloads"
    if not os.path.exists(path):
        os.mkdir(path)
        print("\n~~~ Folder %s created!" % path)
    else:
        print("\n~~~ Folder %s already exists" % path)

    # Dump result to json
    filename = "payloads/payload_users.json"
    print(f"\n~~~ Saving payload in file {filename}")
    with open(filename, "w") as file:
        json.dump(result, file, indent=4)


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def add():
    print("\n~~~ Adding user")
    username = input("\nEnter username to add: ")

    user_payload = {
        "userName": username,
        "description": "Demo User",
        "locale": "en_US",
        "group": ["netadmin"],
        "password": "ypassword",
        "resGroupName": "global",
    }

    url_base = "/dataservice/admin/user"
    result = session.post(url=url_base, json=user_payload).json()
    save_payload(result)


@click.command()
def list():
    url_base = "/dataservice/admin/user"
    result = session.get(url=url_base).json()["data"]
    print("\n~~~ Users\n")
    for item in result:
        print(f" - username: {item['userName']}, group: {item['group']}")
    save_payload(result)


@click.command()
def delete():
    print("\n~~~ Deleting user")
    username = input("\nEnter username to delete: ")
    url_base = f"/dataservice/admin/user/{username}"
    result = session.delete(url=url_base).json()
    save_payload(result)


if __name__ == "__main__":

    # Add commands
    cli.add_command(list)
    cli.add_command(add)
    cli.add_command(delete)

    # Create session
    session = create_session()

    # Run commands
    cli()

    session.close()
