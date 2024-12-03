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


import urllib3
from catalystwan.session import create_manager_session


class MyManager:

    def __init__(self):
        self.status = False
        self.url = None
        self.user = None
        self.password = None
        self.port = 443
        self.profile_id_table = []
        self.config_group_table = []

    def create_session(self, url, user, password):
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
        print(f"Application Version: {self.session.about().application_version}\n")

        self.status = True

    def close(self):
        self.session.close()


class SDRoutingFeatureProfile:
    def __init__(self, manager, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self.manager = manager

        url_base = "dataservice/v1/feature-profile/sd-routing/"

        match self.type:
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
                exit(f"{self.profile_type} type not supported")

        # Get profile_id payload
        # NOTE: details option has been added in 20.12
        url = urlp + self.id + "?details=true"
        self.payload = self.manager.session.get(url).json()
        self.profile_name = self.payload["profileName"]
        self.profile_type = self.payload["profileType"]
        self.solution = self.payload["solution"]


class SDRoutingProfileTable:
    def __init__(self, manager: MyManager):

        self.manager = manager
        self.profiles_table = []

        url_base = "dataservice/v1/feature-profile/sd-routing/"

        # Get list of profiles
        data = self.manager.session.get(url_base).json()

        # Get profile details using profile_id
        for item in data:
            profile_name = item["profileName"]
            profile_id = item["profileId"]
            profile_type = item["profileType"]
            profile = SDWANFeatureProfile(self.manager, profile_id, profile_name, profile_type)
            self.profiles_table.append(profile)

    def list(self):
        print(f"\n~~~ SD-Routing Feature Profiles\n")
        for i in range(len(self.profiles_table)):
            id = self.profiles_table[i].id
            name = self.profiles_table[i].name
            type = self.profiles_table[i].type
            solution = self.profiles_table[i].solution
            print(f"> Profile Name ❯ {name} - {id} - {type} ({solution})")

    def list_categories(self):
        print(f"\n~~~ SD-Routing Feature Profiles per category\n")

        categories = [
            "system",
            "transport",
            "service",
            "cli",
            "policy-object",
        ]

        for item in categories:
            for i in range(len(self.profiles_table)):
                type = self.profiles_table[i].type
                if type == item:
                    id = self.profiles_table[i].id
                    name = self.profiles_table[i].name
                    type = self.profiles_table[i].type
                    solution = self.profiles_table[i].solution
                    print(f"> Profile Name ❯ {name} - {id} - {type} ({solution})")

    def save_profiles(self, workdir):

        print(f"\n~~~ Saving SD-Routing Feature Profiles in {workdir.root}\n")

        for i in range(len(self.profiles_table)):
            profile_id = self.profiles_table[i].id
            profile_name = self.profiles_table[i].name
            profile_type = self.profiles_table[i].type
            profile_solution = self.profiles_table[i].solution
            profile_payload = self.profiles_table[i].payload

            print(
                f"> Saving Profiles name ❯ {profile_name} - id: {profile_id} - type: {profile_type} ({profile_solution}) "
            )

            match profile_type:
                case "system":
                    type = "sdrouting_system"
                case "transport":
                    type = "sdrouting_transport"
                case "service":
                    type = "sdrouting_service"
                case "cli":
                    type = "sdrouting_cli"
                case "policy-object":
                    type = "sdrouting_policy"
                case _:
                    exit(f"{profile_type} type not supported")

            workdir.save(profile_payload, profile_name, type)


class SDWANFeatureProfile:
    def __init__(self, manager, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self.manager = manager

        url_base = "dataservice/v1/feature-profile/sdwan/"

        match self.type:
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
                exit(f"{self.profile_type} type not supported")

        # Get profile_id payload
        # NOTE: details option has been added in 20.12
        url = urlp + self.id + "?details=true"
        self.payload = self.manager.session.get(url).json()
        self.profile_name = self.payload["profileName"]
        self.profile_type = self.payload["profileType"]
        self.solution = self.payload["solution"]


class SDWANProfileTable:
    def __init__(self, manager: MyManager):

        self.manager = manager
        self.profiles_table = []

        url_base = "dataservice/v1/feature-profile/sdwan/"

        # Get list of profiles
        data = self.manager.session.get(url_base).json()

        # Get profile details using profile_id
        for item in data:
            profile_name = item["profileName"]
            profile_id = item["profileId"]
            profile_type = item["profileType"]
            profile = SDWANFeatureProfile(self.manager, profile_id, profile_name, profile_type)
            self.profiles_table.append(profile)

    def list(self):
        print(f"\n~~~ SD-WAN Feature Profiles\n")
        for i in range(len(self.profiles_table)):
            id = self.profiles_table[i].id
            name = self.profiles_table[i].name
            type = self.profiles_table[i].type
            solution = self.profiles_table[i].solution
            print(f"> Profile Name ❯ {name} - {id} - {type} ({solution})")

    def list_categories(self):
        print(f"\n~~~ SD-WAN Feature Profiles per category\n")

        categories = [
            "system",
            "transport",
            "service",
            "cli",
            "policy-object",
        ]

        for item in categories:
            for i in range(len(self.profiles_table)):
                type = self.profiles_table[i].type
                if type == item:
                    id = self.profiles_table[i].id
                    name = self.profiles_table[i].name
                    type = self.profiles_table[i].type
                    solution = self.profiles_table[i].solution
                    print(f"> Profile Name ❯ {name} - {id} - {type} ({solution})")

    def save_profiles(self, workdir):

        print(f"\n~~~ Saving Feature Profiles in {workdir.root}\n")

        for i in range(len(self.profiles_table)):
            profile_id = self.profiles_table[i].id
            profile_name = self.profiles_table[i].name
            profile_type = self.profiles_table[i].type
            profile_solution = self.profiles_table[i].solution
            profile_payload = self.profiles_table[i].payload

            print(
                f"> Saving Profiles name ❯ {profile_name} - id: {profile_id} - type: {profile_type} ({profile_solution}) "
            )

            match profile_type:
                case "system":
                    type = "sdwan_system"
                case "transport":
                    type = "sdwan_transport"
                case "service":
                    type = "sdwan_service"
                case "cli":
                    type = "sdwan_cli"
                case "policy-object":
                    type = "sdwan_policy"
                case _:
                    exit(f"{profile_type} type not supported")

            workdir.save(profile_payload, profile_name, type)


class ConfigGroup:
    def __init__(self, manager, id, name):
        self.id = id
        self.name = name
        self.associated_profiles = 0
        self.manager = manager
        self.profile_table = []
        self.device_table = []
        self.nb_devices = 0
        self.device_payload = ""
        self.value_payload = ""

        url_base = "dataservice/v1/config-group/"

        # Get config-group profiles payload
        url = url_base + self.id
        self.payload = self.manager.session.get(url).json()

    def get_profiles(self):
        for item in self.payload["profiles"]:
            profile_name = item["name"]
            profile_id = item["id"]
            profile_type = item["type"]
            new_element = [profile_id, profile_name, profile_type]
            self.profile_table.append(new_element)
            self.associated_profiles = self.associated_profiles + 1

    def get_devices(self):
        """
        'v1/config-group/{configGroupId}/device/associate'
        """

        url_base = "dataservice/v1/config-group/"
        url_end = "/device/associate"
        url = url_base + self.id + url_end
        data = self.manager.session.get(url).json()

        # Check if there are associated devices
        for key in data["devices"]:
            device_id = key["id"]
            if device_id != "":
                self.nb_devices += 1
                self.device_payload = data
                self.device_table.append(device_id)

    def get_values(self):
        """
        'v1/config-group/{configGroupId}/device/variables'
        """

        url_base = "dataservice/v1/config-group/"
        url_end = "/device/variables"
        url = url_base + self.id + url_end

        if self.nb_devices != 0:
            self.value_payload = self.manager.session.get(url).json()


class ConfigGroupTable:
    def __init__(self, manager: MyManager):
        """
        'v1/config-group'
        """

        self.manager = manager
        self.config_group_table = []

        # API endpoint
        url_base = "dataservice/v1/config-group/"

        # Get payload
        data = self.manager.session.get(url_base).json()

        for key in data:
            config_group_id = key["id"]
            config_group_name = key["name"]
            config_group = ConfigGroup(self.manager, config_group_id, config_group_name)
            config_group.get_profiles()
            config_group.get_devices()
            config_group.get_values()
            self.config_group_table.append(config_group)

    def list_groups(self):
        print(f"\n~~~ Config Groups\n")
        for i in range(len(self.config_group_table)):
            id = self.config_group_table[i].id
            name = self.config_group_table[i].name
            profile_table = self.config_group_table[i].profile_table
            print(f"> Config Group ID ❯ {id} - name: {name}")
            for j in range(len(profile_table)):
                profile_id = profile_table[j][0]
                profile_name = profile_table[j][1]
                profile_type = profile_table[j][2]
                print(f"  - profile-id: {profile_id} - name: {profile_name} - type: {profile_type} ")

    def save_groups(self, workdir):
        """
        List all config-groups with their profiles
        Save config-group payloads in files
        """

        print(f"\n~~~ Saving Config Groups in {workdir.root}\n")

        for i in range(len(self.config_group_table)):
            group_id = self.config_group_table[i].id
            group_name = self.config_group_table[i].name
            group_payload = self.config_group_table[i].payload
            device_payload = self.config_group_table[i].device_payload
            value_payload = self.config_group_table[i].value_payload
            nb_devices = self.config_group_table[i].nb_devices

            # Save config-group payload in file
            print(f"> Saving Config Group name ❯ {group_name} - ID: {group_id} - devices: {nb_devices}")
            workdir.save(group_payload, group_name, "groups")
            if nb_devices != 0:
                workdir.save(device_payload, group_name, "associated")
                workdir.save(value_payload, group_name, "values")
