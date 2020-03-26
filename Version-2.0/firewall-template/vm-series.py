# Copyright 2016 Google Inc. All rights reserved.
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
    """Creates the VM-Series virtual firewall.
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """

    prefix = context.env['deployment']
    resources = []

    loadbalancer_name = prefix + '-loadbalancer' +  context.properties['region']

    if context.properties['network-exist']:
        mgmt_network_ref = (COMPUTE_URL_BASE + 'projects/' + context.env['project'] + 
                            '/global/' + 'networks/' + context.properties['mgmt-network'])
        mgmt_subnet_ref = (COMPUTE_URL_BASE + 'projects/' + context.env['project'] + '/regions/' + 
                           context.properties['region']+ '/subnetworks/' + context.properties['mgmt-subnet'])
        trust_network_ref = (COMPUTE_URL_BASE + 'projects/' + context.env['project'] + 
                             '/global/' + 'networks/' + context.properties['trust-network'])
        trust_subnet_ref = (COMPUTE_URL_BASE + 'projects/' + context.env['project'] + '/regions/' + 
                            context.properties['region']+ '/subnetworks/' + context.properties['trust-subnet'])
        untrust_network_ref = (COMPUTE_URL_BASE + 'projects/' + context.env['project'] + 
                               '/global/' + 'networks/' + context.properties['untrust-network'])
        untrust_subnet_ref = (COMPUTE_URL_BASE + 'projects/' + context.env['project'] + '/regions/' + 
                              context.properties['region']+ '/subnetworks/' + context.properties['untrust-subnet'])
    else:
        mgmt_network_ref = '$(ref.' + context.properties['mgmt-network']+ '.selfLink)'
        mgmt_subnet_ref = '$(ref.' + context.properties['mgmt-subnet'] + '.selfLink)'
        trust_network_ref = '$(ref.' + context.properties['trust-network']+ '.selfLink)'
        trust_subnet_ref = '$(ref.' + context.properties['trust-subnet'] + '.selfLink)'
        untrust_network_ref = '$(ref.' + context.properties['untrust-network']+ '.selfLink)'
        untrust_subnet_ref = '$(ref.' + context.properties['untrust-subnet'] + '.selfLink)'

    it_name = prefix + '-it'

    resources.append({
        'name': it_name,
        'type': 'compute.v1.instanceTemplate',
        'properties': {
            'properties': {
                'labels': {'vm-series-fw-template-version': context.properties['vm-series-fw-template-version']},
                'machineType': context.properties['machine-type'],
                'canIpForward': True,
                #'noAddress': True,
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': ''.join([COMPUTE_URL_BASE, 'projects/',
                                                  'paloaltonetworksgcp-public','/global/',
                                                  'images/',context.properties['image']])
                    }   
                }], 
                'metadata': {
                    'items': [{'key': 'mgmt-interface-swap','value': 'enable'},
                        {'key': 'vmseries-bootstrap-gce-storagebucket','value': context.properties['bootstrap-bucket']},
                        {'key': 'ssh-keys', 'value':context.properties['sshkey']},
                        {'key': 'serial-port-enable','value':'1'}]
                },
                'tags': {
                    'items': [context.properties['fw-instance-tag']],
                },
                'serviceAccounts': [{
                    'email': context.properties['service-account'],
                    'scopes': [
                            'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                            'https://www.googleapis.com/auth/devstorage.read_only',
                            'https://www.googleapis.com/auth/logging.write',
                            'https://www.googleapis.com/auth/monitoring.write',
                    ]}  
                ],  
                'networkInterfaces': [{
                    'network': untrust_network_ref,
                    'subnetwork': untrust_subnet_ref
                },{   
                    'network': mgmt_network_ref,
                    #'accessConfigs': [{
                    #    'name': 'External NAT',
                    #    'type': 'ONE_TO_ONE_NAT'
                    #}], 
                    'subnetwork': mgmt_subnet_ref
                },{   
                    'network': trust_network_ref,
                    'subnetwork': trust_subnet_ref
                }]   
            }   
        }
    })

    namedPorts = []
    for index, portName in enumerate(context.properties['urlPath-namedPort-maps']):
        if context.properties['lb-type'] == 'alb':
            namedPorts.append({'name': portName['appName'], 'port': portName['namedPort']})
        elif context.properties['lb-type'] == 'nlb':
            namedPorts.append({'name': portName['appName'], 'port': context.properties['forwarding-rule-port']})

    for zone in context.properties['zones']:
        igm_name = prefix + '-igm-' + zone
        as_name = prefix + '-as-' + zone

        igm_object = {
            'name': igm_name,
            'type': 'compute.v1.instanceGroupManager',
            'properties': {
                'zone': zone,
                'targetSize': context.properties['min-size'],
                'baseInstanceName': prefix + '-' + zone,
                'namedPorts': namedPorts,
                'instanceTemplate': '$(ref.' + it_name + '.selfLink)' 
            }
        }

        if context.properties['lb-type'] == 'nlb':
            targetpool_name = prefix + '-target-pool-' + context.properties['region']
            igm_object['properties']['targetPools'] = ['$(ref.' + targetpool_name + '.selfLink)']
        resources.append(igm_object)
        
        resources.append({
            'name': as_name,
            'type': 'compute.v1.autoscaler',
            'properties': {
                'zone':zone,
                'target': '$(ref.' + igm_name + '.selfLink)',
                'autoscalingPolicy': {
                    # Given that it takes 7 minutes for a PA-VM
                    # to become functional, we need a cool down time
                    # period of 10 minutes for a new autoscale event
                    # to kick in.
                    'coolDownPeriodSec': 600,
                    'maxNumReplicas': context.properties['max-size'],
                    'minNumReplicas': context.properties['min-size'],
                    "customMetricUtilizations": [{
                        "metric": context.properties['metric'],
                        "utilizationTargetType": context.properties['target-type'],
                        "utilizationTarget": context.properties['util-target']
                    }]
                }
            }
        })
        
    return { 'resources': resources }
