import json
import os
from os.path import join


def print_payload(data):
    with open("payload.log", "w") as file:
        json.dump(data, file, indent=4)


class Workdir:
    def __init__(self, dir):
        """
        Create output folder structure
        """

        self.root = join(os.path.abspath(os.getcwd()), dir)

        # create config-group folders
        cg_dir = ["groups", "associated", "values"]
        for dir in cg_dir:
            try:
                os.makedirs(os.path.join(self.root, "config_groups", dir))
            except OSError:
                pass

        # Create sdwan feature-profiles folders
        fp_dir = ["cli", "service", "system", "transport", "policy_objects"]
        for dir in fp_dir:
            try:
                os.makedirs(os.path.join(self.root, "feature_profiles", "sdwan", dir))
            except OSError:
                pass

        # Create sdrouting feature-profiles folders
        fp_dir = ["cli", "service", "system", "transport", "policy_objects"]
        for dir in fp_dir:
            try:
                os.makedirs(os.path.join(self.root, "feature_profiles", "sd_routing", dir))
            except OSError:
                pass

    def save(self, payload, name, type):
        """
        Save API json payload into a file
        """

        match type:
            case "groups":
                current_dir = self.root + "/config_groups/groups"
            case "values":
                current_dir = self.root + "/config_groups/values"
            case "associated":
                current_dir = self.root + "/config_groups/associated"
            case "sdwan_cli":
                current_dir = self.root + "/feature_profiles" + "/sdwan" + "/cli"
            case "sdwan_system":
                current_dir = self.root + "/feature_profiles" + "/sdwan" + "/system"
            case "sdwan_transport":
                current_dir = self.root + "/feature_profiles" + "/sdwan" + "/transport"
            case "sdwan_service":
                current_dir = self.root + "/feature_profiles" + "/sdwan" + "/service"
            case "sdwan_policy":
                current_dir = self.root + "/feature_profiles" + "/sdwan" + "/policy_objects"
            case "sdrouting_cli":
                current_dir = self.root + "/feature_profiles" + "/sd_routing" + "/cli"
            case "sdrouting_system":
                current_dir = self.root + "/feature_profiles" + "/sd_routing" + "/system"
            case "sdrouting_transport":
                current_dir = self.root + "/feature_profiles" + "/sd_routing" + "/transport"
            case "sdrouting_service":
                current_dir = self.root + "/feature_profiles" + "/sd_routing" + "/service"
            case "sdrouting_policy":
                current_dir = self.root + "/feature_profiles" + "/sd_routing" + "/policy_objects"
            case _:
                exit(f"{type} type not supported")

        tmp = name + ".json"
        filename = join(current_dir, tmp)
        with open(filename, "w") as file:
            json.dump(payload, file, indent=4)
