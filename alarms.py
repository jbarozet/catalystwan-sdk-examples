from catalystwan.dataclasses import Severity

from session import create_session

# Create vManage session
session = create_session()


def print_alarm(item):
    print(f"system-ip: {item.system_ip}, host: {item.hostname} , severity: {item.severity}")


# Get alarms
alarms = session.api.alarms.get()
print("~~~ ALARMS ~~~~~~~~~~~~~~~~~")
for item in alarms:
    print_alarm(item)

# To get all not viewed alarms:
not_viewed_alarms = session.api.alarms.get().filter(viewed=False)
print("~~~ ALARMS - not viewed ~~~~~~~~~~~~~~~~~")
for item in not_viewed_alarms:
    print_alarm(item)


# To get all alarms from past n hours:
n = 24
alarms_from_n_hours = session.api.alarms.get(from_time=n)

# To get all critical alarms from past n hours:
n = 48
critical_alarms = session.api.alarms.get(from_time=n).filter(severity=Severity.CRITICAL)
print("~~~ ALARMS - critical ~~~~~~~~~~~~~~~~~")
for item in critical_alarms:
    print_alarm(item)
