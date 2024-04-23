# =========================================================
# Catalyst SD-WAN Backup Task
#
# Description:
#   Backup config-groups and feature profiles
#   Backup devices associated with config-group
#   Backup deployment values
#
# Backup data hierarchy:
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
#       policy_object
#
# Author: jbarozet@gmail.com
# Last updated: 2024-03-21
#

import json
import logging
import os
from datetime import datetime
from os.path import join

import urllib3
from catalystwan.api.config_group_api import ConfigGroupAPI, ConfigGroupResponsePayload
from catalystwan.session import ManagerHTTPError

from session import create_session

logger = logging.getLogger("catalystwan")
profile_id_table = []
config_group_table = []


def create_backup_dir():
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    workdir = "data/" + current_datetime
    # os.mkdir(workdir)
    # Check if workdir folder already exists. If yes, then stop backup process
    workdir = join(os.path.abspath(os.getcwd()), workdir)
    if os.path.isdir(workdir):
        exit(
            f"{workdir} folder is already in use. Please select a different workdir directory."
        )

    # create config-group folders
    cg_dir = ["groups", "associated", "values"]
    for dir in cg_dir:
        os.makedirs(os.path.join(workdir, "config_groups", dir))

    # Create feature-profiles folders
    fp_dir = ["cli", "service", "system", "transport"]
    for dir in fp_dir:
        os.makedirs(os.path.join(workdir, "feature_profiles", dir))

    return workdir


def save_config_groups(rootdir):
    """
    List specific config-group details
    Get the list of feature profiles used but not parcels
    Need to use the API for profiles to get the list of associated parcels
    """

    url_base = "dataservice/v1/config-group/"
    workdir = rootdir + "/config_groups/groups"

    # Get payload
    data = session.get(url_base).json()

    print("\n--- Saving Config Groups")

    for key in data:
        config_group_id = key["id"]
        config_group_name = key["name"]
        new_element = [config_group_name, config_group_id, 0]
        config_group_table.append(new_element)

        tmp = config_group_name + ".json"
        filename = join(workdir, tmp)
        print(f"> Config Group ID ❯ {config_group_name}")

        # Get config-group profiles payload
        url = url_base + config_group_id
        config_group = session.get(url).json()

        # save all associated feature-profiles in a table
        for item in config_group["profiles"]:
            profile_id = item["id"]
            profile_type = item["type"]
            new_element = [profile_id, profile_type]
            profile_id_table.append(new_element)
            print(new_element)

        # Save config-group payload in file
        with open(filename, "w") as file:
            json.dump(config_group, file, indent=4)


def save_feature_profiles(rootdir):
    """
    Feature Profiles - Get specific profile details
    Including associated parcels
    """

    url_base = "dataservice/v1/feature-profile/sdwan/service/"
    workdir_cli = rootdir + "/feature_profiles/cli"
    workdir_system = rootdir + "/feature_profiles/system"
    workdir_transport = rootdir + "/feature_profiles/transport"
    workdir_service = rootdir + "/feature_profiles/service"

    print("\n--- Saving Features Profiles")

    for i in range(len(profile_id_table)):
        profile_id = profile_id_table[i][0]
        profile_type = profile_id_table[i][1]

        match profile_type:
            case "system":
                workdir = workdir_system
            case "transport":
                workdir = workdir_transport
            case "service":
                workdir = workdir_service
            case "cli":
                workdir = workdir_cli
            case _:
                exit(f"{profile_type} type not supported")

        # Get payload
        # NOTE: details option has been added in 20.12
        url = url_base + profile_id + "?details=true"
        data = session.get(url).json()

        profile_name = data["profileName"]
        tmp = profile_name + ".json"

        print(f"> Profile Name ❯ {profile_name} - {profile_id} - {profile_type}")

        # Save feature-profiles in file
        filename = join(workdir, tmp)
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)


def save_associated_devices(rootdir):
    """
    Get Devices associated with a specific config-group.
    'v1/config-group/{configGroupId}/device/associate'
    """

    url_base = "dataservice/v1/config-group/"
    url_end = "/device/associate"
    workdir = rootdir + "/config_groups/associated"

    print("\n--- Saving associated devices")

    for i in range(len(config_group_table)):
        config_group_name = config_group_table[i][0]
        config_group_id = config_group_table[i][1]

        print(f"> Config Group ❯ {config_group_name} - {config_group_id}")

        url = url_base + config_group_id + url_end
        data = session.get(url).json()

        # Check if there are associated devices
        nb_devices = 0
        for key in data["devices"]:
            device_id = key["id"]
            if device_id != "":
                nb_devices = nb_devices + 1
                print(f"device_id: {device_id}")

        # Save number of devices associated with selected config-group
        config_group_table[i][2] = nb_devices

        # Save file only if there are devices
        if nb_devices != 0:
            tmp = config_group_name + ".json"
            filename = join(workdir, tmp)
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)


def save_config_group_values(rootdir):
    """
    'v1/config-group/{configGroupId}/device/variables'
    """

    url_base = "dataservice/v1/config-group/"
    url_end = "/device/variables"
    workdir = rootdir + "/config_groups/values"

    print("\n--- Saving device deployment values")

    for i in range(len(config_group_table)):
        config_group_name = config_group_table[i][0]
        config_group_id = config_group_table[i][1]
        config_group_devices = config_group_table[i][2]
        url = url_base + config_group_id + url_end

        print(
            f"> Config Group ❯ {config_group_name} with {config_group_devices} associated"
        )

        if config_group_devices != 0:
            data = session.get(url).json()
            tmp = config_group_name + ".json"
            filename = join(workdir, tmp)
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)


def save_automated_rules():
    # base = "dataservice/tag/tagRules/"
    # base = "v1/config-group/{configGroupId}/rules"
    base = "dataservice/v1/config-group/"
    config_group_id = input("Enter config-group id: ")
    url = base + config_group_id + "/rules"
    data = session.get(url).json()
    data_formatted = json.dumps(data, indent=4)
    print(data_formatted)


# Disable warnings because of no certificate on vManage
# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create vManage session
session = create_session()

# Create backup folder hierarchy
rootdir = create_backup_dir()

# Save device configs
save_config_groups(rootdir)
save_feature_profiles(rootdir)
save_associated_devices(rootdir)
save_config_group_values(rootdir)
# save_automated_rules()
