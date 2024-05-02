# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Device Config
# Using Config Group and Feature Profiles
#
# Description:
#   Get config-groups and feature profiles
#   Get devices associated with config-group
#   Get deployment values
#
# Output data hierarchy:
#   config_groups
#       associated
#       groups
#       values
#
#   feature_profiles
#       cli
#       system
#       transport
#       service
#       policy-object
#
# =========================================================================

import json
import os
from os.path import join

import click

from session import create_session

workdir_base = "data/outputs/"

# feature-profiles: id, type
profile_id_table = []

# config-group: id, name, number of devices
config_group_table = []


def create_workdir():
    """
    Create output folder structure
    """
    # current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # workdir = "data/outputs/" + current_datetime
    workdir = "data/outputs/"
    # os.mkdir(workdir)
    # Check if workdir folder already exists. If yes, then stop backup process
    workdir = join(os.path.abspath(os.getcwd()), workdir)
    # if os.path.isdir(workdir):
    #     exit(f"{workdir} folder is already in use. Please select a different workdir directory.")

    # create config-group folders
    cg_dir = ["groups", "associated", "values"]
    for dir in cg_dir:
        try:
            os.makedirs(os.path.join(workdir, "config_groups", dir))
        except OSError:
            pass

    # Create feature-profiles folders
    fp_dir = ["cli", "service", "system", "transport", "policy-objects"]
    for dir in fp_dir:
        try:
            os.makedirs(os.path.join(workdir, "feature_profiles", dir))
        except OSError:
            pass

    return workdir


def save_output(payload, name, type):
    """
    Save API json payload into a file
    """

    match type:
        case "groups":
            current_dir = workdir + "/config_groups/groups"
        case "cli":
            current_dir = workdir + "/feature_profiles" + "/cli"
        case "system":
            current_dir = workdir + "/feature_profiles" + "/system"
        case "transport":
            current_dir = workdir + "/feature_profiles" + "/transport"
        case "service":
            current_dir = workdir + "/feature_profiles" + "/service"
        case "policy-object":
            current_dir = workdir + "/feature_profiles" + "/policy-objects"
        case _:
            exit(f"{type} type not supported")

    tmp = name + ".json"
    filename = join(current_dir, tmp)

    with open(filename, "w") as file:
        json.dump(payload, file, indent=4)


@click.group()
def cli():
    """Command line tool to showcase Catalyst SD-WAN Python SDK"""
    pass


@click.command()
def list_groups():
    """
    List all config-groups with their profiles
    Save payloads in files
    """

    # API endpoint
    url_base = "dataservice/v1/config-group/"

    # Get payload
    data = session.get(url_base).json()

    print(f"\n~~~ Saving Config Groups in {workdir}\n")

    for key in data:
        config_group_id = key["id"]
        config_group_name = key["name"]
        new_element = [config_group_name, config_group_id, 0]
        config_group_table.append(new_element)

        print(f"> Config Group ID ❯ {config_group_name}")

        # Get config-group profiles payload
        url = url_base + config_group_id
        config_group = session.get(url).json()

        # save all associated feature-profiles in a table
        for item in config_group["profiles"]:
            profile_name = item["name"]
            profile_id = item["id"]
            profile_type = item["type"]
            new_element = [profile_id, profile_type]
            profile_id_table.append(new_element)
            print(f"  - profile-name: {profile_name} -type: {profile_type}, id: {profile_id}")

        # Save config-group payload in file
        save_output(config_group, config_group_name, "groups")


@click.command()
def list_profiles_summary():
    """Feature Profiles - Get all profiles"""

    base = "dataservice/v1/feature-profile/sdwan/"
    data = session.get(base).json()
    i = 0
    for item in data:
        data_formatted = json.dumps(data[i], indent=4)
        print(data_formatted)
        i = i + 1


@click.command()
def list_profiles():
    """
    List Feature Profiles with details and parcels
    Save payloads in files
    """

    url_base = "dataservice/v1/feature-profile/sdwan/"

    print("\n~~~ Saving Features Profiles in {workdir}\n")

    # Get list of profiles
    data = session.get(url_base).json()

    # Get profile details using profile_id
    for item in data:
        profile_name = item["profileName"]
        profile_id = item["profileId"]
        profile_type = item["profileType"]

        match profile_type:
            case "system":
                urlp = url_base + "system/"
            case "transport":
                urlp = url_base + "transport/"
            case "service":
                urlp = url_base + "service/"
            case "cli":
                urlp = url_base + "cli/"
            case "policy-object":
                urlp = url_base + "policy-object/"
            case _:
                exit(f"{profile_type} type not supported")

        # Get profile_id payload
        # NOTE: details option has been added in 20.12
        url = urlp + profile_id + "?details=true"
        data = session.get(url).json()

        profile_name = data["profileName"]
        print(f"> Profile Name ❯ {profile_name} - {profile_id} - {profile_type}")
        save_output(data, profile_name, profile_type)


@click.command()
def list_profiles_categories():
    """
    List Feature Profiles per category:
        - system
        - transport
        - service
        - cli
        - policy-object
    """

    categories = [
        "dataservice/v1/feature-profile/sdwan/system",
        "dataservice/v1/feature-profile/sdwan/transport",
        "dataservice/v1/feature-profile/sdwan/service",
        "dataservice/v1/feature-profile/sdwan/cli",
        "dataservice/v1/feature-profile/sdwan/policy-object",
    ]

    for item in categories:
        data = session.get(item).json()
        i = 0
        for item in data:
            data_formatted = json.dumps(data[i], indent=4)
            print(data_formatted)
            i = i + 1


cli.add_command(list_groups)
cli.add_command(list_profiles)
cli.add_command(list_profiles_summary)
cli.add_command(list_profiles_categories)

session = create_session()
workdir = create_workdir()

if __name__ == "__main__":
    cli()
