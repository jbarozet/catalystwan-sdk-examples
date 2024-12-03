# Create/List/Delete user
# To enable log:
# export catalystwan_devel=1
# That will create a catalystwan.log file

import sys

sys.path.insert(0, "..")
from catalystwan.api.administration import User
from catalystwan.session import ManagerSession

from utils.session import create_session


# Get the list of users
def list_users(session: ManagerSession):
    users = session.api.users.get()

    print("\n~~~ Users")
    for user in users:
        print(f" - {user.username} > group: {user.group} - resource-group:{user.resource_group}")


# Create a new user
def create_user(session: ManagerSession):
    new_user = User(username="test2", password="test!@#", group=["netadmin"], description="Test")
    session.api.users.create(new_user)


# Delete a user
def delete_user(session: ManagerSession):
    session.api.users.delete(username="test2")


def run_demo():
    with create_session() as session:
        create_user(session)
        # list_users(session)
        # delete_user(session)
        # list_users(session)


if __name__ == "__main__":
    run_demo()
