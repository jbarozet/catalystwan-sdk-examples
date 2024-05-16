from session import create_session

# Create session
session = create_session()


# ----------------------------------------------------------------------------------------------------
# API Get the list of users
# ----------------------------------------------------------------------------------------------------

users = session.api.users.get()

# ----------------------------------------------------------------------------------------------------
# Display the list of devices
# ----------------------------------------------------------------------------------------------------

print("\n~~~ Users")

for user in users:
    print(f" - {user.username} > group: {user.group} - resource-group:{user.resource_group}")
