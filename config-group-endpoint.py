from session import create_session

# Create session
session = create_session()

# Get the list of Config Groups
configuration_groups = session.endpoints.configuration_group
config_groups = configuration_groups.get()

for group in config_groups:
    cg_name = group.name
    cg_solution = group.solution
    cg_description = group.description
    print(
        f"\nname: {cg_name} - solution: {cg_solution} - description: {cg_description}"
    )
    cg_profiles = group.profiles
    for profile in cg_profiles:
        profile_id = profile.id
        profile_description = profile.description
        profile_type = profile.type
        profile_created_on = profile.created_on
        profile_created_by = profile.created_by
        print(f" > profile: {profile_id}")
        print(f"    - type: {profile_type}")
        print(f"    - description: {profile_description}")
        print(f"    - created by: {profile_created_by} on {profile_created_on}")


# =========================================================================================
# BACKUP
# =========================================================================================
#
# configuration_groups = session.endpoints.configuration_group
# config_group_table = configuration_groups.get()
# Display Config Groups
# for i in range(len(config_group_table)):
#     cg_name = config_group_table[i].name
#     cg_solution = config_group_table[i].solution
#     cg_description = config_group_table[i].description
#     print(f"name: {cg_name} - solution: {cg_solution} - description: {cg_description}")
#     profile_table = config_group_table[i].profiles
#     for x in range(len(profile_table)):
#         print(f"- profiles: {profile_table[x].id} - {profile_table[x].type}")

# ----------------------------------------------------------------------------------------------------
# APIs - Config Groups
# ----------------------------------------------------------------------------------------------------

# using api - same output
# cg = session.api.config_group
# cg_table = cg.get()
# print(cg_table)
# print("")
