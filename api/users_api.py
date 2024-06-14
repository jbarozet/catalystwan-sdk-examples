import sys

sys.path.insert(0, "..")

from catalystwan.api.administration import User

from session import create_session

# Create session
session = create_session()

# API Get the list of users
users = session.api.users.get()

# Display the list of devices
print("\n~~~ Users")

for user in users:
    print(f" - {user.username} > group: {user.group} - resource-group:{user.resource_group}")

new_user = User(userName="test", password="test!@#", group=["netadmin"], description="Test")
session.api.users.create(new_user)

session.close()
