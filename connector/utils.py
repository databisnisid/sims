from .drivers.snmp import get
from location.models import Location
from connector.models import Device
from pysnmp import hlapi
import platform
import subprocess


def ping(host_or_ip, packets=1, timeout=1000):
    """ Calls system "ping" command, returns True if ping succeeds.
    Required parameter: host_or_ip (str, address of host to ping)
    Optional parameters: packets (int, number of retries), timeout (int, ms to wait for response)
    Does not show any output, either as popup window or in command line.
    Python 3.5+, Windows and Linux compatible
    """
    # The ping command is the same for Windows and Linux, except for the "number of packets" flag.
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
        # run parameters: capture output, discard error messages, do not show window
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=0x08000000)
        # 0x0800000 is a windows-only Popen flag to specify that a new process will not create a window.
        # On Python 3.7+, you can use a subprocess constant:
        #   result = subprocess.run(command, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        # On windows 7+, ping returns 0 (ok) when host is not reachable; to be sure host is responding,
        # we search the text "TTL=" on the command output. If it's there, the ping really had a response.
        return result.returncode == 0 and b'TTL=' in result.stdout
    else:
        command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]
        # run parameters: discard output and error messages
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0


COMMUNITY = 'public'
# SNMP_OID = '1.3.6.1.4.1'


def update_parameter_status():
    """ Update all parameter status in location model using connector.utils """

    location = Location.objects.all()

    for loc in location:
        # Ping First
        ping_result = ping(loc.ipaddress)

        # print(ping_result)
        loc.ping_status = ping_result

        if loc.device is not None and ping_result is True:

            # Get Product Type if Device Type is Blank
            if loc.device.parameter_type is not None and loc.device_type is None:
                result = get(loc.ipaddress, [loc.device.parameter_type], hlapi.CommunityData(COMMUNITY))

                if result is None:
                    loc.device = None
                else:
                    loc.device_type = result[loc.device.parameter_type]

                loc.save()

            # Get Product Type if Device Type contains OID
            """
            if SNMP_OID in loc.device.type:
                device = Device.objects.get(id=loc.device.id)
                result = get(loc.ipaddress, [device.type], hlapi.CommunityData(COMMUNITY))
                device.type = result[device.type]
                device.save()
            """

        if loc.device is not None and ping_result is True:
            values = []
            if loc.device.parameter_1.value is not None:
                values += [loc.device.parameter_1.value]
            if loc.device.parameter_2.value is not None:
                values += [loc.device.parameter_2.value]
            if loc.device.parameter_3.value is not None:
                values += [loc.device.parameter_3.value]
            if loc.device.parameter_4.value is not None:
                values += [loc.device.parameter_4.value]

            if values is not None:
                result_parameter = get(loc.ipaddress, values, hlapi.CommunityData(COMMUNITY))

                if result_parameter:
                    if loc.parameter_1:
                        print(loc.device.parameter_1.value, result_parameter[loc.device.parameter_1.value])
                        loc.status_1 = result_parameter[loc.device.parameter_1.value]
                        print(loc.status_1)

                    if loc.parameter_2:
                        print(loc.device.parameter_2.value, result_parameter[loc.device.parameter_2.value])
                        loc.status_2 = result_parameter[loc.device.parameter_2.value]
                        print(loc.status_2)

                    if loc.parameter_3:
                        print(loc.device.parameter_3.value, result_parameter[loc.device.parameter_3.value])
                        loc.status_3 = result_parameter[loc.device.parameter_3.value]
                        print(loc.status_3)

                    if loc.parameter_4:
                        print(loc.device.parameter_4.value, result_parameter[loc.device.parameter_4.value])
                        loc.status_4 = result_parameter[loc.device.parameter_4.value]
                        print(loc.status_4)

                    loc.save()
