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

vm_series_fw_template_version = "1-0-0"

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Deploy VM-Series virtual firewall templates.
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """

    resources = []

    prefix = context.env['deployment']
    network_exist = False
    if ('mgmt-network' in context.properties and 'mgmt-subnet' in context.properties 
         and 'trust-network' in context.properties and 'trust-subnet' in context.properties 
         and 'untrust-network' in context.properties and 'untrust-subnet' in context.properties):
        mgmt_network_name = context.properties['mgmt-network']
        mgmt_subnet_name = context.properties['mgmt-subnet']
        trust_network_name = context.properties['trust-network']
        trust_subnet_name = context.properties['trust-subnet']
        untrust_network_name = context.properties['untrust-network']
        untrust_subnet_name = context.properties['untrust-subnet']
        network_exist = True
    else: 
        mgmt_network_name = prefix + '-' + 'mgmt-nw' 
        mgmt_subnet_name = prefix + '-' + 'mgmt-sn'
        resources.append({
            'name': mgmt_network_name,
            'type': 'network.py'
        })
        resources.append({
            'name': mgmt_subnet_name,
            'type': 'subnetwork.py',
            'properties': {
                'network': mgmt_network_name,
                'ipcidrrange': context.properties['mgmt-network-cidr'],
                'region': context.properties['region']
            }  
        }) 

        trust_network_name = prefix + '-' + 'trust-nw'
        trust_subnet_name = prefix + '-' + 'trust-sn'
        resources.append({
            'name': trust_network_name,
            'type': 'network.py'
        })
        resources.append({
            'name': trust_subnet_name,
            'type': 'subnetwork.py',
            'properties': {
                'network': trust_network_name,
                'ipcidrrange': context.properties['trust-network-cidr'],
                'region': context.properties['region']
            }
        })
 
        untrust_network_name = prefix + '-' + 'untrust-nw' 
        untrust_subnet_name = prefix + '-' + 'untrust-sn' 
        resources.append({
            'name': untrust_network_name,
            'type': 'network.py'
        })
        resources.append({
            'name': untrust_subnet_name,
            'type': 'subnetwork.py',
            'properties': {
                'network': untrust_network_name,
                'ipcidrrange': context.properties['untrust-network-cidr'],
                'region': context.properties['region']
            }
        })
    

    if context.properties['cloud-nat']:
        resources.append({
            'name': prefix + '-cloud-nat',
            'type': 'cloud-nat.py',
            'properties': {
                'network': '$(ref.' + mgmt_network_name + '.name)',
                'region': context.properties['region']
            }
        })

    resources.append({
        'name': 'panw-vm',
        'type': 'vm-series.py',
        'properties': {
            'vm-series-fw-template-version': vm_series_fw_template_version,
            'zones': context.properties['zones'],         
            'region': context.properties['region'],         
            'machine-type': context.properties['machine-type'],
            'mgmt-network': mgmt_network_name,
            'mgmt-subnet': mgmt_subnet_name,
            'trust-network': trust_network_name,
            'trust-subnet': trust_subnet_name,
            'untrust-network': untrust_network_name,
            'untrust-subnet': untrust_subnet_name,
            'network-exist': network_exist,
            'image': context.properties['image'],
            'fw-instance-tag': context.properties['fw-instance-tag'],
            'sshkey': context.properties['sshkey'],
            'bootstrap-bucket': context.properties['bootstrap-bucket'],
            'service-account': context.properties['service-account'],
            'urlPath-namedPort-maps': context.properties['urlPath-namedPort-maps'],
            #'size': context.properties['size'],
            'target-type': context.properties['target-type'],
            'util-target': context.properties['util-target'],
            'metric': 'custom.googleapis.com/VMSeries/panSessionActive',
            'max-size': context.properties['max-size'],
            'min-size': context.properties['min-size'],
            'lb-type': context.properties['lb-type'],
            'forwarding-rule-port': context.properties['forwarding-rule-port']
        }   
    })
 
    if 'mgmt-network-access-source-range' in context.properties:
        if 'mgmt-network-access-ports' in context.properties:
            mgmtPorts = ','.join([str(i) for i in context.properties['mgmt-network-access-ports']])
        else:
            mgmtPorts = ''
        resources.append({
            'name': "access-mgmt",
            'type': 'firewall.py',
            'properties': {
                'network': mgmt_network_name,
                'network-exist': network_exist,
                'sourceRange': ','.join(context.properties['mgmt-network-access-source-range']),
                'protocol': 'tcp',
                'ports': mgmtPorts,
                'instance-tag': context.properties['fw-instance-tag']
            }   
        })
    
    if context.properties['lb-type'] == 'alb':
        source_range = '130.211.0.0/22,35.191.0.0/16,209.85.152.0/22,209.85.204.0/22'
    elif context.properties['lb-type'] == 'nlb':
        source_range = '0.0.0.0/0'
    resources.append({
        'name': "hc-untrust",
        'type': 'firewall.py',
        'properties': {
            'network': untrust_network_name,
            'network-exist': network_exist,
            'sourceRange': source_range,
            'protocol': 'tcp',
            'ports': '',
            'instance-tag': context.properties['fw-instance-tag']
        }
    })
    resources.append({
        'name': "allow-trust",
        'type': 'firewall.py',
        'properties': {
            'network': trust_network_name,
            'network-exist': network_exist,
            'sourceRange': '0.0.0.0/0',
            'protocol': 'all',
            'ports': '',
        }
    })

    if context.properties['lb-type'] == 'alb':
        if (context.properties['forwarding-rule-port'] == 443) and ('ssl-certificate-url' in context.properties):
            ssl_certificate = context.properties['ssl-certificate-url']
        else:
            ssl_certificate = '' 
        resources.append({
            'name': 'external-appln-lb',
            'type': 'external-appln-lb.py',
            'properties': {
                'zones': context.properties['zones'],         
                'fw-igm-name':'$(ref.panw-vm.igm-name)',
                'instance-tag': context.properties['fw-instance-tag'],
                'region': context.properties['region'],
                'urlPath-namedPort-maps': context.properties['urlPath-namedPort-maps'],
                'forwarding-rule-port': context.properties['forwarding-rule-port'],
                'connection-draining-timeout': context.properties['connection-draining-timeout'],
                'ssl-certificate-url': ssl_certificate
            }
        })
    elif context.properties['lb-type'] == 'nlb':
        resources.append({
            'name': 'external-network-lb',
            'type': 'external-network-lb.py',
            'properties': {
                'region': context.properties['region'],
                'backEndPort': context.properties['forwarding-rule-port'],
                'forwarding-rule-port': context.properties['forwarding-rule-port'],
                'appName': context.properties['urlPath-namedPort-maps'][0]['appName']
            }
        })

    return {
        'resources': resources,
        'outputs': [
            {'name': 'trust-network-name',
            'value': trust_network_name},
            {'name': 'trust-subnet-name',
            'value': trust_subnet_name},
            {'name': 'deployment-name',
            'value': prefix}
        ]
    }
