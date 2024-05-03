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
#   Save everything under output folder
#
# Output folder hierarchy:
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

import urllib3
from catalystwan.session import create_manager_session


class MyManager:

    def __init__(self, url, user, password, workdir):
        """
        url: url or ip address
        user: user name
        password: user password
        dir: folder name to use to save files
        """

        self.url = url
        self.user = user
        self.password = password
        self.port = 443
        self.profile_id_table = []
        self.config_group_table = []
        self.workdir = workdir

        # Disable warnings because of no certificate on vManage
        # urllib3.disable_warnings()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.session = create_manager_session(url=self.url, username=self.user, password=self.password)

        self.version = self.session.about().version
        self.api_version = self.session.api_version
        self.application_version = self.session.about().application_version

        print("\n~~~ Session Information\n")
        print(f"vManage: {self.session.url}")
        print(f"Version: {self.session.about().version}")
        print(f"API Version: {self.session.api_version}")
        print(f"Application Version: {self.session.about().application_version}")

        self.status = True

    def save_groups(self):
        """
        List all config-groups with their profiles
        Save payloads in files
        """

        # API endpoint
        url_base = "dataservice/v1/config-group/"

        # Get payload
        data = self.session.get(url_base).json()

        print(f"\n~~~ Saving Config Groups in {self.workdir.root}\n")

        for key in data:
            config_group_id = key["id"]
            config_group_name = key["name"]
            new_element = [config_group_name, config_group_id, 0]
            self.config_group_table.append(new_element)

            print(f"> Config Group ID ❯ {config_group_name}")

            # Get config-group profiles payload
            url = url_base + config_group_id
            config_group = self.session.get(url).json()

            # save all associated feature-profiles in a table
            for item in config_group["profiles"]:
                profile_name = item["name"]
                profile_id = item["id"]
                profile_type = item["type"]
                new_element = [profile_id, profile_type]
                self.profile_id_table.append(new_element)
                print(f"  - profile-name: {profile_name} -type: {profile_type}, id: {profile_id}")

            # Save config-group payload in file
            self.workdir.save(config_group, config_group_name, "groups")

    def save_associated_devices(self):
        """
        Get Devices associated with a specific config-group.
        'v1/config-group/{configGroupId}/device/associate'
        """

        url_base = "dataservice/v1/config-group/"
        url_end = "/device/associate"

        print(f"\n~~~ Saving associated devices in {self.workdir.root}\n")

        for i in range(len(self.config_group_table)):
            config_group_name = self.config_group_table[i][0]
            config_group_id = self.config_group_table[i][1]

            print(f"> Config Group ❯ {config_group_name} - {config_group_id}")

            url = url_base + config_group_id + url_end
            data = self.session.get(url).json()

            # Check if there are associated devices
            nb_devices = 0
            for key in data["devices"]:
                device_id = key["id"]
                if device_id != "":
                    nb_devices = nb_devices + 1
                    print(f"  - device_id: {device_id}")

            # Save number of devices associated with selected config-group
            self.config_group_table[i][2] = nb_devices

            # Save file only if there are devices
            if nb_devices != 0:
                self.workdir.save(data, config_group_name, "associated")
                # tmp = config_group_name + ".json"
                # filename = join(current_dir, tmp)
                # with open(filename, "w") as file:
                #     json.dump(data, file, indent=4)

    def save_config_group_values(self):
        """
        'v1/config-group/{configGroupId}/device/variables'
        """

        url_base = "dataservice/v1/config-group/"
        url_end = "/device/variables"

        print(f"\n~~~ Saving device deployment values in {self.workdir.root}\n")

        for i in range(len(self.config_group_table)):
            config_group_name = self.config_group_table[i][0]
            config_group_id = self.config_group_table[i][1]
            config_group_devices = self.config_group_table[i][2]
            url = url_base + config_group_id + url_end

            print(f"> Config Group ❯ {config_group_name} with {config_group_devices} associated")

            if config_group_devices != 0:
                data = self.session.get(url).json()
                self.workdir.save(data, config_group_name, "values")
                # tmp = config_group_name + ".json"
                # filename = join(current_dir, tmp)
                # with open(filename, "w") as file:
                #     json.dump(data, file, indent=4)

    def save_sdwan_profiles(self):
        """
        List Feature Profiles with details and parcels
        Save payloads in files
        """

        url_base = "dataservice/v1/feature-profile/sdwan/"

        print(f"\n~~~ Saving SD-WAN Features Profiles in {self.workdir.root}\n")

        # Get list of profiles
        data = self.session.get(url_base).json()

        # Get profile details using profile_id
        for item in data:
            profile_name = item["profileName"]
            profile_id = item["profileId"]
            profile_type = item["profileType"]

            match profile_type:
                case "system":
                    urlp = url_base + "system/"
                    type = "sdwan_system"
                case "transport":
                    urlp = url_base + "transport/"
                    type = "sdwan_transport"
                case "service":
                    urlp = url_base + "service/"
                    type = "sdwan_service"
                case "cli":
                    urlp = url_base + "cli/"
                    type = "sdwan_cli"
                case "policy-object":
                    urlp = url_base + "policy-object/"
                    type = "sdwan_policy"
                case _:
                    exit(f"{profile_type} type not supported")

            # Get profile_id payload
            # NOTE: details option has been added in 20.12
            url = urlp + profile_id + "?details=true"
            data = self.session.get(url).json()

            profile_name = data["profileName"]
            print(f"> Profile Name ❯ {profile_name} - {profile_id} - {profile_type}")
            self.workdir.save(data, profile_name, type)

    def save_sdrouting_profiles(self):
        """
        List Feature Profiles with details and parcels
        Save payloads in files
        """

        url_base = "dataservice/v1/feature-profile/sd-routing/"

        print(f"\n~~~ Saving SD-Routing Features Profiles in {self.workdir.root}\n")

        # Get list of profiles
        data = self.session.get(url_base).json()

        # Get profile details using profile_id
        for item in data:
            profile_name = item["profileName"]
            profile_id = item["profileId"]
            profile_type = item["profileType"]

            match profile_type:
                case "system":
                    urlp = url_base + "system/"
                    type = "sdrouting_system"
                case "transport":
                    urlp = url_base + "transport/"
                    type = "sdrouting_transport"
                case "service":
                    urlp = url_base + "service/"
                    type = "sdrouting_service"
                case "cli":
                    urlp = url_base + "cli/"
                    type = "sdrouting_cli"
                case "policy-object":
                    urlp = url_base + "policy/"
                    type = "sdrouting_policy"
                case _:
                    exit(f"{profile_type} type not supported")

            # Get profile_id payload
            # NOTE: details option has been added in 20.12
            url = urlp + profile_id + "?details=true"
            data = self.session.get(url).json()

            profile_name = data["profileName"]
            print(f"> Profile Name ❯ {profile_name} - {profile_id} - {profile_type}")
            self.workdir.save(data, profile_name, type)

    def list_sdwan_profiles_summary(self):
        """Feature Profiles - Get all profiles"""

        base = "dataservice/v1/feature-profile/sdwan/"

        print("\n~~~ List of SD-WAN Features Profiles\n")

        data = self.session.get(base).json()

        # Get profile details using profile_id
        for item in data:
            profile_name = item["profileName"]
            profile_id = item["profileId"]
            profile_type = item["profileType"]
            solution = item["solution"]

            print(f"> Profile Name ❯ {profile_name} - {solution} - {profile_id} - {profile_type}")

    def list_sdrouting_profiles_summary(self):
        """Feature Profiles - Get all profiles"""

        base = "dataservice/v1/feature-profile/sd-routing/"

        print("\n~~~ List of SD-Routing Features Profiles\n")

        data = self.session.get(base).json()

        # Get profile details using profile_id
        for item in data:
            profile_name = item["profileName"]
            profile_id = item["profileId"]
            profile_type = item["profileType"]
            solution = item["solution"]

            print(f"> Profile Name ❯ {profile_name} - {solution} - {profile_id} - {profile_type}")

    def list_profiles_categories(self):
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
            data = self.session.get(item).json()
            for item in data:
                profile_name = item["profileName"]
                profile_id = item["profileId"]
                profile_type = item["profileType"]
                solution = item["solution"]

                print(f"> Profile Name ❯ {profile_name} - {solution} - {profile_id} - {profile_type}")

    def list_automated_rules(self):
        # base = "dataservice/tag/tagRules/"
        # base = "v1/config-group/{configGroupId}/rules"
        base = "dataservice/v1/config-group/"
        config_group_id = input("Enter config-group id: ")
        url = base + config_group_id + "/rules"
        data = self.session.get(url).json()
        data_formatted = json.dumps(data, indent=4)
        print(data_formatted)
