# Copyright 2017 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'


def GenerateConfig(context):
    """Build an internal load balancer (regionBackendService).
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """

    prefix = context.env['deployment']

    healthcheck_name = prefix + '-hc-' + context.properties['region']
    loadbalancer_name = prefix + '-lb-' +  context.properties['region']
    forwardingrule_name = prefix + '-fr-' + context.properties['region']
    host_project = context.properties['host-project']

    network_ref = COMPUTE_URL_BASE + 'projects/' + host_project + '/global/' + 'networks/' + context.properties['network']
    subnet_ref = COMPUTE_URL_BASE + 'projects/' + host_project + '/regions/' + context.properties['region']+ '/subnetworks/' + context.properties['subnet']

    resources = []

    resources.append({
        'name': healthcheck_name,
        'type': 'compute.v1.healthCheck',
        'properties': {
            'type': 'TCP',
            'tcpHealthCheck': {
                'port': context.properties['ilb-port']
            },
        }
    }) 

    backends = []
    for zone in context.properties['zones']:
        igm_name = prefix + '-igm-' + zone
        backends.append({
            'name': loadbalancer_name + '-be' + zone,
            'group': '$(ref.' + igm_name + '.instanceGroup)'})
    resources.append({
        'name': loadbalancer_name,
        'type': 'compute.v1.regionBackendService',
        'properties': {
            'region': context.properties['region'],
            'network': context.properties['network'],
            'healthChecks': ['$(ref.' + healthcheck_name + '.selfLink)'],
            'backends': backends, 
            'protocol': 'TCP',
            'loadBalancingScheme': 'INTERNAL',
        }
    })

    resources.append({
        'name': forwardingrule_name,
        'type': 'compute.v1.forwardingRule',
        'properties': {
            'ports': [context.properties['ilb-port']],
            'network': network_ref,
            'subnetwork': subnet_ref,
            'region': context.properties['region'],
            'backendService': '$(ref.' + loadbalancer_name + '.selfLink)',
            'loadBalancingScheme': 'INTERNAL',
        }
    })
  
    return {
        'resources': resources,
        'outputs': [{
            'name': 'ilb-ip',
            'value': '$(ref.' + forwardingrule_name + '.IPAddress)'
        }, {
            'name': 'ilb-port',
            'value': '$(ref.' + forwardingrule_name + '.ports[0])'
        }]
    }

