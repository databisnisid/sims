from .drivers import snmp, http, ping
from location.models import Location
from pysnmp import hlapi
from django.utils import timezone


COMMUNITY = 'public'


def update_parameter_status():
    """ Update all parameter status in location model using connector.utils """

    location = Location.objects.all()

    for loc in location:
        # Ping First
        ping_result = ping.ping(loc.ipaddress)
        loc.ping_status = ping_result
        print('PING', loc.ipaddress, ping_result)
        loc.save()

        if loc.device is not None and ping_result is True:
            # Get Product Type if Device Type is Blank
            print(loc.device.connector)
            if loc.device.connector == 'SNMP':
                if loc.device.parameter_type is not None and not loc.device_type.strip():
                    update_snmp_device_type(loc)
                update_snmp_parameters(loc)

            if loc.device.connector == 'HTTP':
                print('Check HTTP')
                update_http_parameters(loc)


def construct_http_url(ipaddress, parameter):
    """ Construct URL """
    return parameter.replace('__IPADDRESS__', ipaddress)


def get_http_status(url):
    """ Get Status of Device """
    result, is_image_ok = http.get(url)
    status = False
    if result:
        if is_image_ok:
            status = True

    return status


def get_http_parameter(ipaddress, parameter):
    """ Get Status per Parameter """
    return get_http_status(construct_http_url(ipaddress, parameter))


def values_array(loc):
    """ Return Array list of Parameter value """
    values = []

    if loc.device.parameter_1.value is not None:
        values += [loc.device.parameter_1.value]
    if loc.device.parameter_2.value is not None:
        values += [loc.device.parameter_2.value]
    if loc.device.parameter_3.value is not None:
        values += [loc.device.parameter_3.value]
    if loc.device.parameter_4.value is not None:
        values += [loc.device.parameter_4.value]

    return values


def update_http_parameters(loc):
    """ Get Parameter Status for HTTP Connector """
    values = values_array(loc)
    status = {}

    print(values)
    for value in values:
        status[value] = 1 if (get_http_parameter(loc.ipaddress, value)) is True else 0

    loc.status_1 = status[loc.device.parameter_1.value]
    loc.status_2 = status[loc.device.parameter_2.value]
    loc.status_3 = status[loc.device.parameter_3.value]
    loc.status_4 = status[loc.device.parameter_4.value]

    print('HTTP Status', loc.status_1, loc.status_2, loc.status_3, loc.status_4)

    loc.save()


def update_snmp_device_type(loc):
    """ Get Product Type if Device Type is Blank """
    try:
        result = snmp.get(loc.ipaddress, [loc.device.parameter_type.value], hlapi.CommunityData(COMMUNITY))
    except RuntimeError:
        result = None

    if result is None:
        print('Remove Device', loc.device, 'from', loc.name)
        loc.device = None
    else:
        loc.device_type = result[loc.device.parameter_type.value]
        print('Get Result', loc.device_type, 'for', loc.name)

    loc.save()


def update_snmp_parameters(loc):
    """ Get SNMP Status for each Parameter """
    values = values_array(loc)

    if values is not None:
        try:
            result = snmp.get(loc.ipaddress, values, hlapi.CommunityData(COMMUNITY))
        except RuntimeError:
            result = None

        if result:
            loc.status_1 = result[loc.device.parameter_1.value] if loc.parameter_1 is True else 0
            loc.status_2 = result[loc.device.parameter_2.value] if loc.parameter_2 is True else 0
            loc.status_3 = result[loc.device.parameter_3.value] if loc.parameter_3 is True else 0
            loc.status_4 = result[loc.device.parameter_4.value] if loc.parameter_4 is True else 0
            print('SNMP Status', loc.status_1, loc.status_2, loc.status_3, loc.status_4)

            loc.save()
