""" This template creates a Cloud NAT. """

def generate_config(context):
    """ Entry point for the deployment resources. """
    prefix = context.env['deployment']
    name = context.properties.get('name', context.env['name'])

    resources = [
        {
            'name': name + '-router',
            'type': 'compute.v1.router',
            'properties':
                {
                    'name': name,
                    'network': generate_network_url(context),
                    'region': context.properties['region'],
                    'nats':
                    [{
                        'name': name,
                        # Force using All subnet all primary IP range by default
                        # Force using one of the two enums below:
                        # ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES and
                        # ALL_SUBNETWORKS_ALL_IP_RANGES
                        'sourceSubnetworkIpRangesToNat': context.properties.get(
                            'sourceSubnetworkIpRangesToNat',
                            'ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES'),
                        'natIps': context.properties.get('natIps', []),
                        'natIpAllocateOption': 'MANUAL_ONLY' if context.properties.get('natIps') else 'AUTO_ONLY',
                        'minPortsPerVm': context.properties.get(
                            'minPortsPerVm', 64),
                        'udpIdleTimeoutSec': context.properties.get(
                            'udpIdleTimeoutSec', 30),
                        'icmpIdleTimeoutSec': context.properties.get(
                            'icmpIdleTimeoutSec', 30),
                        'tcpEstablishedIdleTimeoutSec': context.properties.get(
                            'tcpEstablishedIdleTimeoutSec', 1200),
                        'tcpTransitoryIdleTimeoutSec': context.properties.get(
                            'tcpTransitoryIdleTimeoutSec', 30)
                    }]
                }
        }
    ]

    return {
        'resources':
            resources,
        'outputs':
            [
                {
                    'name': 'name',
                    'value': name
                }
            ]
    }


def generate_network_url(context):
    """Format the resource name as a resource URI."""

    return 'projects/{}/global/networks/{}'.format(
        context.env['project'],
        context.properties['network']
    )
