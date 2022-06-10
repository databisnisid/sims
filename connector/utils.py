from .drivers.snmp import get
from location.models import Location
import pyping
from pysnmp import hlapi

COMMUNITY = 'public'


def update_parameter_status():

    location = Location.objects.filter().exclude(device=None)

    for loc in location:
        # Ping First
        import pyping
        ping = pyping.ping(loc.ipaddress)

        print(ping.ret_code)
        loc.ping_status = ping.ret_code

        values = []
        values += [loc.device.parameter_1.value]
        values += [loc.device.parameter_2.value]
        values += [loc.device.parameter_3.value]
        values += [loc.device.parameter_4.value]

        result = get(loc.ipaddress, values, hlapi.CommunityData(COMMUNITY))

        #print(result)
        if loc.parameter_1:
            print(loc.device.parameter_1.value, result[loc.device.parameter_1.value])
            loc.status_1 = result[loc.device.parameter_1.value]
            print(loc.status_1)

        if loc.parameter_2:
            print(loc.device.parameter_2.value, result[loc.device.parameter_2.value])
            loc.status_2 = result[loc.device.parameter_2.value]
            print(loc.status_2)

        if loc.parameter_3:
            print(loc.device.parameter_3.value, result[loc.device.parameter_3.value])
            loc.status_3 = result[loc.device.parameter_3.value]
            print(loc.status_3)

        if loc.parameter_4:
            print(loc.device.parameter_4.value, result[loc.device.parameter_4.value])
            loc.status_4 = result[loc.device.parameter_4.value]
            print(loc.status_4)

        loc.save()
