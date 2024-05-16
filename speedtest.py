from session import create_session

# Create vManage session
session = create_session()


def speedtest():
    source_device = session.api.devices.get().filter(hostname="edge1").single_or_default()
    destination_device = session.api.devices.get().filter(hostname="edge2").single_or_default()

    speedtest = session.api.speedtest.speedtest(source_device, destination_device)

    print(f"Upload is: {speedtest.up_speed} Mbps, download is: {speedtest.down_speed} Mbps")

    if speedtest.up_speed > 100 and speedtest.down_speed > 100:
        print(
            "Speedtest succeeded for devices: source - '{speedtest.device_name}', destination - '{speedtest.destination_name}'"
        )
    else:
        print(
            f"Speedtest failed for devices: source - '{speedtest.device_name}', destination - '{speedtest.destination_name}'"
        )


if __name__ == "__main__":
    speedtest()
