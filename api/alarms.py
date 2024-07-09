import sys

import click

sys.path.insert(0, "..")
from catalystwan.dataclasses import Severity

from utils.session import create_session

# Create vManage session
session = create_session()


def print_alarm(item):
    print(f"system-ip: {item.system_ip}, host: {item.hostname} , severity: {item.severity}")


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def get_alarms():
    """
    Get all alarms
    """
    alarms = session.api.alarms.get()
    print("~~~ ALARMS ~~~~~~~~~~~~~~~~~")
    for item in alarms:
        print_alarm(item)


@click.command()
def get_non_viewed_alarms():
    """
    To get all not viewed alarms
    """
    not_viewed_alarms = session.api.alarms.get().filter(viewed=False)
    print("~~~ ALARMS - not viewed ~~~~~~~~~~~~~~~~~")
    for item in not_viewed_alarms:
        print_alarm(item)


@click.command()
def get_alarms_from_last24h():
    """
    To get all alarms from past n hours
    """
    n = 24
    alarms_from_n_hours = session.api.alarms.get(from_time=n)

    print("~~~ ALARMS - not viewed ~~~~~~~~~~~~~~~~~")
    for item in alarms_from_n_hours:
        print_alarm(item)


@click.command()
def get_alarms_critical_from_last24h():
    """
    To get all critical alarms from past n hours
    """

    n = 48
    critical_alarms = session.api.alarms.get(from_time=n).filter(severity=Severity.CRITICAL)
    print("~~~ ALARMS - critical ~~~~~~~~~~~~~~~~~")
    for item in critical_alarms:
        print_alarm(item)


cli.add_command(get_alarms)
cli.add_command(get_non_viewed_alarms)
cli.add_command(get_alarms_from_last24h)
cli.add_command(get_alarms_critical_from_last24h)


# Main
if __name__ == "__main__":
    cli()
