import json
import click
from session import create_session


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def list_config_groups():
    """
    List all config-groups with their profiles
    But do not list parcels
    """

    base = "dataservice/v1/config-group/"
    data = session.get(base).json()
    i = 0
    for item in data:
        data_formatted = json.dumps(data[i], indent=4)
        print(data_formatted)
        i = i + 1


@click.command()
def list_config_group_details():
    """
    List specific config-group details
    But do not list parcels
    """

    base = "dataservice/v1/config-group/"
    data = session.get(base).json()

    for key in data:
        config_group_id = key["id"]
        print(f"---- Config Group ID: {config_group_id} ----------------- ")
        url = base + config_group_id
        config_group = session.get(url).json()
        data_formatted = json.dumps(config_group, indent=4)
        print(data_formatted)


@click.command()
def list_feature_profiles():
    """Feature Profiles - Get all profiles"""

    base = "dataservice/v1/feature-profile/sdwan/"
    data = session.get(base).json()
    i = 0
    for item in data:
        data_formatted = json.dumps(data[i], indent=4)
        print(data_formatted)
        i = i + 1


@click.command()
def list_feature_profiles_categories():
    """
    Feature Profiles
    - system profiles: dataservice/v1/feature-profile/sdwan/system
    - cli profiles: dataservice/v1/feature-profile/sdwan/cli
    - service profiles: dataservice/v1/feature-profile/sdwan/service
    - transport profiles: dataservice/v1/feature-profile/sdwan/transport
    """

    print("--- System Profiles ----------------")
    base = "dataservice/v1/feature-profile/sdwan/system"
    data = session.get(base).json()
    i = 0
    for item in data:
        data_formatted = json.dumps(data[i], indent=4)
        print(data_formatted)
        i = i + 1

    print("--- Transport Profiles ----------------")
    base = "dataservice/v1/feature-profile/sdwan/transport"
    data = session.get(base).json()
    i = 0
    for item in data:
        data_formatted = json.dumps(data[i], indent=4)
        print(data_formatted)
        i = i + 1

    print("--- Service Profiles ----------------")
    base = "dataservice/v1/feature-profile/sdwan/service"
    data = session.get(base).json()
    i = 0
    for item in data:
        data_formatted = json.dumps(data[i], indent=4)
        print(data_formatted)
        i = i + 1


@click.command()
def list_feature_profile_details():
    """
    Feature Profiles - Get specific profile details
    Including associated parcels
    """

    base = "dataservice/v1/feature-profile/sdwan/system/"
    feature_profile_id = input("Enter feature-profile ID ❯ ")
    url = base + feature_profile_id
    data = session.get(url).json()
    data_formatted = json.dumps(data, indent=4)
    print(data_formatted)


cli.add_command(list_config_groups)
cli.add_command(list_config_group_details)
cli.add_command(list_feature_profiles)
cli.add_command(list_feature_profiles_categories)
cli.add_command(list_feature_profile_details)

session = create_session()

if __name__ == "__main__":
    cli()
