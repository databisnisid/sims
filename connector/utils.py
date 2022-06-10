from .drivers.snmp import get
from location.models import Location
from .models import Device
from pysnmp import hlapi


COMMUNITY = 'public'


def get_parameter_status():

    location = Location.objects.filter().exclude(device=None)

    for loc in location:
        values = []
        values += [loc.device.parameter_1.value]
        values += [loc.device.parameter_2.value]
        values += [loc.device.parameter_3.value]
        values += [loc.device.parameter_4.value]

        result = get(loc.ipaddress, values,hlapi.CommunityData(COMMUNITY))

        print(result)