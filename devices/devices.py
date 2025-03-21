# Get devices
#
#
import sys

import click
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.feature_profile.sdwan.system import bfd
from tabulate import tabulate

sys.path.insert(0, "..")
from catalystwan.dataclasses import Personality

from utils.session import create_session


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def all():
    with create_session() as session:
        devices = session.api.devices.get()
        count = session.api.devices.count_devices(personality=Personality.EDGE)

        print(f"\nNumber of WAN Edge devices in the fabric: {count}")

        table = list()
        headers = ["Device Name", "System IP", "Serial", "UUID", "Reachable"]

        for dev in devices:
            tr = [
                dev.hostname,
                dev.local_system_ip,
                dev.board_serial,
                dev.uuid,
                dev.is_reachable,
            ]
            table.append(tr)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def edges():
    with create_session() as session:
        devices = session.api.devices.get()
        count = session.api.devices.count_devices(personality=Personality.EDGE)
        edges = devices.filter(personality=Personality.EDGE)

        print(f"\nNumber of WAN Edge devices in the fabric: {count}")

        table = list()
        headers = ["Device Name", "System IP", "Serial", "UUID", "Reachable"]

        for dev in edges:
            tr = [
                dev.hostname,
                dev.local_system_ip,
                dev.board_serial,
                dev.uuid,
                dev.is_reachable,
            ]
            table.append(tr)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
@click.option("--system_ip", help="System IP address of the device")
def interface_status(system_ip):
    """Retrieve and return information about Interface status of network device
    Example command: python devices-raw.py interface-status --system_ip 10.0.0.1
    """

    with create_session() as session:
        devices = session.api.devices.get()
        edges = devices.filter(personality=Personality.EDGE)

        # Create a list of device IPs
        device_ips = [dev.local_system_ip for dev in edges]

        # Check if the provided system_ip is in our device list
        if system_ip not in device_ips:
            click.echo(f"Error: Device with system IP {system_ip} not found in the network.")
            return

        transport_interfaces = session.api.device_state.get_device_wan_interfaces(system_ip)

        table = list()
        headers = ["Name", "State", "Operational State", "Color", "Private IP", "Private Port", "Public IP", "Public Port"]

        for item in transport_interfaces:
            tr = [
                item.interfaceName,
                item.adminState,
                item.operationalState,
                item.color,
                item.privateIp,
                item.privatePort,
                item.publicIp,
                item.publicPort,
            ]
            table.append(tr)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
@click.option("--system_ip", help="System IP address of the device")
def bfd_sessions(system_ip):
    """Retrieve and return information about bfd sessions for a router
    Example command: python devices-raw.py bfd_sessions --system_ip 10.0.0.1
    """

    with create_session() as session:
        devices = session.api.devices.get()
        edges = devices.filter(personality=Personality.EDGE)

        # Create a list of device IPs
        device_ips = [dev.local_system_ip for dev in edges]

        # Check if the provided system_ip is in our device list
        if system_ip not in device_ips:
            click.echo(f"Error: Device with system IP {system_ip} not found in the network.")
            return

        bfd_sessions = session.api.device_state.get_bfd_sessions(system_ip)

        table = list()
        headers = ["State", "Source TLOC", "Remote TLOC", "DeviceIP", "SourceIP", "DestinationIP"]

        for dev in bfd_sessions:
            tr = [
                dev.state,
                dev.sourceTlocColor,
                dev.remoteTlocColor,
                dev.deviceIp,
                dev.sourceIp,
                dev.destinationPublicIp,
            ]
            table.append(tr)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def edges_reachable():
    with create_session() as session:
        devices = session.api.devices.get()
        count = session.api.devices.count_devices(personality=Personality.EDGE)
        reachable = devices.filter(personality=Personality.EDGE, reachability="reachable")

        print(f"\nNumber of WAN Edge devices in the fabric: {count}")

        table = list()
        headers = ["Device Name", "System IP", "Serial", "UUID", "Reachable"]

        for dev in reachable:
            tr = [
                dev.hostname,
                dev.local_system_ip,
                dev.board_serial,
                dev.uuid,
                dev.is_reachable,
            ]
            table.append(tr)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def edge_details():
    edge_name = input("\nEnter device name: ")

    with create_session() as session:
        devices = session.api.devices.get()
        edge_device = devices.filter(hostname=edge_name).single_or_default()

        if edge_device is not None:
            print(f" - Edge: {edge_device.hostname} - uuid: {edge_device.uuid} - cpu: {edge_device.cpu_load}")
        else:
            print("Device not found")


@click.command()
def controllers():
    with create_session() as session:
        devices = session.api.devices.get()

        table = list()
        headers = ["Device Name", "System IP", "Serial", "UUID", "Reachable"]

        vmanages = devices.filter(personality=Personality.VMANAGE)

        for dev in vmanages:
            tr = [
                dev.hostname,
                dev.local_system_ip,
                dev.board_serial,
                dev.uuid,
                dev.is_reachable,
            ]
            table.append(tr)

        vbonds = devices.filter(personality=Personality.VBOND)

        for dev in vbonds:
            tr = [
                dev.hostname,
                dev.local_system_ip,
                dev.board_serial,
                dev.uuid,
                dev.is_reachable,
            ]
            table.append(tr)

        vsmarts = devices.filter(personality=Personality.VSMART)

        for dev in vsmarts:
            tr = [
                dev.hostname,
                dev.local_system_ip,
                dev.board_serial,
                dev.uuid,
                dev.is_reachable,
            ]
            table.append(tr)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))


@click.command()
def health():
    with create_session() as session:
        # Device Health
        device_health = session.api.dashboard.get_devices_health_overview()
        print("\n~~~ Device Health Summary")

        table = list()
        headers = ["Good", "Fair", "Poor"]
        tr = [
            device_health.single_or_default().good,
            device_health.single_or_default().fair,
            device_health.single_or_default().poor,
        ]

        table.append(tr)

        # Align all columns to the left
        colalign = ["left"] * len(headers)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid", colalign=colalign))

        # Tunnel Health

        print("\n~~~ Tunnel Health Summary")

        tunnel_health = session.api.dashboard.get_tunnel_health()

        table = list()
        headers = ["Tunnel Name", "VQoE Score", "Health", "Latency", "Jitter", "Loss"]

        for item in tunnel_health:
            health_color = item.health.split(".")[-1] if isinstance(item.health, str) else item.health.name
            tr = [
                item.name,
                item.vqoe_score,
                health_color,
                item.latency,
                item.jitter,
                item.loss_percentage,
            ]
            table.append(tr)

        # Align all columns to the left
        colalign = ["left"] * len(headers)

        click.echo(tabulate(table, headers, tablefmt="fancy_grid", colalign=colalign))


if __name__ == "__main__":
    # Add commands
    cli.add_command(all)
    cli.add_command(edges)
    cli.add_command(interface_status)
    cli.add_command(bfd_sessions)
    cli.add_command(edges_reachable)
    cli.add_command(edge_details)
    cli.add_command(controllers)
    cli.add_command(health)

    # Run commands
    cli()


# ---END---
