from contextlib import contextmanager
from dataclasses import dataclass
from uuid import UUID

from catalystwan.session import ManagerSession
from service_profile import ServiceProfile
from system_profile import SystemProfile
from transport_profile import TransportProfile

from utils.session import create_session

null_uuid = UUID("00000000-0000-0000-0000-000000000000")


@dataclass
class ProfileIds:
    config_group_id: UUID
    system_profile_id: UUID
    transport_profile_id: UUID
    service_profile_id: UUID


class ConfigGroup:
    def __init__(self, session: ManagerSession):
        self.session = session
        self.config_group_api = self.session.api.sdwan_feature_profiles.system

        # Config group properties
        self.config_group_name = "SDK_ConfigGroup"
        self.config_group_description = "Config Group from SDK"
        self.config_group_solution = "sdwan"

        # IDs initialized with null UUID
        self.config_group_id = null_uuid
        self.system_profile_id = null_uuid
        self.transport_profile_id = null_uuid

        # Profile instances
        self.system_profile = SystemProfile(session)
        self.transport_profile = TransportProfile(session)
        self.service_profile = ServiceProfile(session)

    def create(self) -> None:
        """Create config group with the given profile IDs."""

        # Create associated feature profiles
        self.create_profiles()

        print(f"\nConfiguring Config Group: {self.config_group_name}")

        self.config_group_id = self.session.api.config_group.create(
            name=self.config_group_name,
            description=self.config_group_description,
            solution="sdwan",
            profile_ids=[
                self.system_profile_id,
                self.transport_profile_id,
                self.service_profile_id,
            ],
        ).id

    def delete(self):
        """Delete config group."""

        # Search config-group based on name
        config_group = self.session.api.config_group.get().filter(name=self.config_group_name).single_or_default()

        if config_group is not None:
            config_group_id = config_group.id
            self.session.api.config_group.delete(config_group_id)
            print(f"- Existing Config Group {self.config_group_name} deleted: {config_group_id}")

        else:
            print(f"- Config Group {self.config_group_name} not found")

        # Delete associated feature profiles
        self.delete_profiles()

    def create_profiles(self) -> None:
        """Create all Feature Profiles"""

        self.system_profile_id = self.system_profile.create()
        self.transport_profile_id = self.transport_profile.create()
        self.service_profile_id = self.service_profile.create()

    def delete_profiles(self) -> None:
        """Delete all associated Feature Profiles"""

        # Check if profile exists and delete
        self.system_profile.delete()
        self.transport_profile.delete()
        self.service_profile.delete()

    def print_summary(self) -> None:
        """Print summary of created profiles and config group."""

        print("\n- Summary")
        print(f"  - ConfigGroup ID: {self.config_group_id}")
        print(f"  - System Profile ID: {self.system_profile_id}")
        print(f"  - Transport Profile ID: {self.transport_profile_id}")
        print(f"  - Service Profile ID: {self.service_profile_id}")


# @contextmanager
# def create_vmanage_session():
#     """Context manager for creating and managing vManage session."""
#     session = None
#     try:
#         session = create_session()
#         yield session
#     finally:
#         if session:
#             session.close()
