import sys
from datetime import datetime

import click
from tabulate import tabulate

sys.path.insert(0, "..")
from catalystwan.dataclasses import Severity

from utils.session import create_session

# Create vManage session
session = create_session()


def print_alarm_table(alarms):
    table_data = []
    for alarm in alarms:
        # Convert Unix timestamp to human readable format
        readable_time = datetime.fromtimestamp(alarm.entry_time / 1000).strftime("%Y-%m-%d %H:%M:%S")

        # Remove "Severity." prefix from severity value
        severity_str = str(alarm.severity)
        if severity_str.startswith("Severity."):
            severity_str = severity_str.replace("Severity.", "")

        table_data.append([readable_time, alarm.system_ip, alarm.hostname, severity_str, alarm.component])

    headers = ["Date", "System IP", "Hostname", "Severity", "Component"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def get_all():
    """
    Get all alarms
    """
    alarms = session.api.alarms.get()
    print("~~~ ALARMS ~~~~~~~~~~~~~~~~~")
    print_alarm_table(alarms)


@click.command()
def get_non_viewed():
    """
    To get all not viewed alarms
    """
    alarms = session.api.alarms.get().filter(viewed=False)
    print("~~~ ALARMS ~~~~~~~~~~~~~~~~~")
    print_alarm_table(alarms)


@click.command()
def get_last():
    """
    To get all alarms from past n hours
    """
    n = 24
    alarms = session.api.alarms.get(from_time=n)
    print(f"~~~ ALARMS - from last {n}h ~~~~~~~~~~~~~~~~~")
    print_alarm_table(alarms)


@click.command()
def get_last_critical():
    """
    To get all critical alarms from past n hours
    """
    n = 24
    alarms = session.api.alarms.get(from_time=n).filter(severity=Severity.CRITICAL)
    print(f"~~~ ALARMS - critical from last {n}h~~~~~~~~~~~~~~~~~")
    print_alarm_table(alarms)


cli.add_command(get_all)
cli.add_command(get_non_viewed)
cli.add_command(get_last)
cli.add_command(get_last_critical)


# Main
if __name__ == "__main__":
    cli()
