from session import create_session

# Create vManage session
session = create_session()

# Get alarms
alarms = session.api.alarms.get()
print(alarms)
