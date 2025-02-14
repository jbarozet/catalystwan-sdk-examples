# =========================================================================
# Catalyst WAN SDK
#
# SD-WAN/SD-Routing UX 2.0 Configuration
# Config Groups, Feature Profiles, Policy Groups
#
# =========================================================================

import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from manager import ConfigGroupTable, MyManager, SDRoutingProfileTable, SDWANProfileTable
from prompt import Prompt

from utils import Workdir


def help():
    print("Define vManage parameters in .env file")
    exit(1)


def backup():
    """
    Save config-groups and feature profiles
    Save devices associated with config-group
    Save deployment values
    Backup data hierarchy:
        config_groups
            associated
            groups
            values
        feature_profiles
            cli
            system
            transport
            service
            policy-object
    """

    if not manager.status:
        print("Session not created")
        return

    # Create backup folder
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    dir = "data/" + current_datetime
    workdir = Workdir(dir)

    config_group_table = ConfigGroupTable(manager)
    config_group_table.save_groups(workdir)
    sdwan_profiles_table = SDWANProfileTable(manager)
    sdwan_profiles_table.save_profiles(workdir)
    sdrouting_profiles_table = SDRoutingProfileTable(manager)
    sdrouting_profiles_table.save_profiles(workdir)


def list_groups():
    if not manager.status:
        logging.error("Session not created")
        return
    config_group_table = ConfigGroupTable(manager)
    config_group_table.list_groups()


def list_sdwan_profiles():
    if not manager.status:
        print("Session not created")
        return
    profiles_table = SDWANProfileTable(manager)
    profiles_table.list()


def list_sdwan_profile_categories():
    if not manager.status:
        print("Session not created")
        return
    profile_table = SDWANProfileTable(manager)
    profile_table.list_categories()


def list_sdrouting_profiles():
    if not manager.status:
        print("Session not created")
        return
    profiles_table = SDRoutingProfileTable(manager)
    profiles_table.list()


def list_sdrouting_profile_categories():
    if not manager.status:
        print("Session not created")
        return
    profile_table = SDRoutingProfileTable(manager)
    profile_table.list_categories()


def quit():
    print("Quitting ...")
    manager.close()
    raise SystemExit


def create_session():
    load_dotenv()

    url = os.getenv("vmanage_host")
    user = os.getenv("vmanage_user")
    password = os.getenv("vmanage_password")

    if url is None or user is None or password is None:
        help()
        exit()

    # Create SD-WAN Manager session
    print(f"Creating session with SD-WAN Manager {url}\n")
    manager.create_session(url, user, password)
    if not manager.status:
        exit(1)


# Main
if __name__ == "__main__":

    logging.basicConfig(
        format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        level=logging.INFO,
    )

    manager = MyManager()
    dir = "data/outputs/"

    options = {
        "Create session with SD-WAN Manager": create_session,
        "Backup Configuration Groups and Feature Profiles": backup,
        "List Configuration Groups": list_groups,
        "List SD-WAN Feature Profiles": list_sdwan_profiles,
        "List SD-WAN Feature Profiles per category": list_sdwan_profile_categories,
        "List SD-Routing Feature Profiles": list_sdrouting_profiles,
        "List SD-Routing Feature Profiles per category": list_sdrouting_profile_categories,
        "Quit": quit,
    }

    while True:
        print("")
        Prompt.dict_menu(options)
