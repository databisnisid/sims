from .drivers import snmp, http, ping
from location.models import Location
from pysnmp import hlapi


COMMUNITY = 'public'


def update_parameter_status():
    """ Update all parameter status in location model using connector.utils """

    location = Location.objects.all()

    for loc in location:
        # Ping First
        ping_result = ping.ping(loc.ipaddress)
        loc.ping_status = ping_result
        loc.save()

        if loc.device is not None and ping_result is True:
            # Get Product Type if Device Type is Blank
            if loc.device.parameter_type is not None and not loc.device_type.strip():
                if loc.device.connector is 'SNMP':
                    update_snmp_device_type(loc)
                    update_snmp_parameters(loc)
                if loc.device.connector is 'HTTP':
                    update_http_parameters(loc)


def construct_http_url(ipaddress, parameter):
    """ Construct URL """
    return 'http://' + ipaddress + '/' + parameter


def get_http_status(url):
    """ Get Status of Device """
    result, is_image_ok = http.get(url)
    if result:
        if is_image_ok:
            status = True
        else:
            status = False
    else:
        status = False

    return status


def get_http_parameter(ipaddress, parameter):
    """ Get Each Parameter Status """
    return get_http_status(construct_http_url(ipaddress, parameter))


def update_http_parameters(loc):
    """ Get Parameter Status for HTTP Connector """
    values = {}

    if loc.device.parameter_1.value is not None:
        values += loc.device.parameter_1.value
    if loc.device.parameter_2.value is not None:
        values += loc.device.parameter_2.value
    if loc.device.parameter_3.value is not None:
        values += loc.device.parameter_3.value
    if loc.device.parameter_4.value is not None:
        values += loc.device.parameter_4.value

    for value in values:
        print(value)
        loc.status_1 = 1 if (get_http_parameter(loc.ipaddress, value)) else loc.status_1
        loc.status_2 = 1 if (get_http_parameter(loc.ipaddress, value)) else loc.status_2
        loc.status_3 = 1 if (get_http_parameter(loc.ipaddress, value)) else loc.status_3
        loc.status_4 = 1 if (get_http_parameter(loc.ipaddress, value)) else loc.status_4

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
        try:
            result = snmp.get(loc.ipaddress, values, hlapi.CommunityData(COMMUNITY))
        except RuntimeError:
            result = None

        if result:
            loc.status_1 = result[loc.device.parameter_1.value] if loc.parameter_1 else loc.status_1
            loc.status_2 = result[loc.device.parameter_2.value] if loc.parameter_2 else loc.status_2
            loc.status_3 = result[loc.device.parameter_3.value] if loc.parameter_3 else loc.status_3
            loc.status_4 = result[loc.device.parameter_4.value] if loc.parameter_4 else loc.status_4

            loc.save()
