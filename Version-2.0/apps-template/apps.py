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

app_template_version = "1-0-0"

def GenerateConfig(context):
    """Deploy application templates.
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """

    resources = [ 
    {
        'name': 'web-vm',
        'type': 'web-vm-example.py',
        'properties': {
            'host-project': context.properties['host-project'],
            'app-template-version': app_template_version,
            'zones': context.properties['zones'],         
            'region': context.properties['region'],         
            'app-machine-type': context.properties['app-machine-type'],
            'trust-network': context.properties['trust-network'],
            'trust-subnet': context.properties['trust-subnet'],
            #'app-image': context.properties['app-image'],
            'app-instance-tag': context.properties['app-instance-tag'],
            'size': 1,
            'utilTarget': 0.8,
            'maxSize': 2,
            'minSize': 1,
            'sshkey': context.properties['sshkey'],
            #'bootstrap-bucket': context.properties['bootstrap-bucket']
        }   
    },
    {
        'name': 'internal-lb',
        'type': 'internal-lb.py',
        'properties': {
            'host-project': context.properties['host-project'],
            'zones': context.properties['zones'],         
            'network': context.properties['trust-network'],
            'subnet': context.properties['trust-subnet'],
            'instance-tag': context.properties['app-instance-tag'],
            'region': context.properties['region'],
            'ilb-port': context.properties['ilb-port'],
        }
    },
    {
        #'metadata': {
        #    'dependsOn': ['internal-lb', 'web-vm', 'forward-rule']
        #},
        'name': 'apps-deployment-pubsub',
        'type': 'pubsub.py',
        'properties': {
            'host-project': context.properties['host-project'],
            'fw-deployment-name': context.properties['fw-deployment-name'],
            'region': context.properties['region'],
            'vm-series-fw-template-topic': context.properties['vm-series-fw-template-topic'], 
            'app-template-version': app_template_version,
            'ilb-ip': '$(ref.internal-lb.ilb-ip)',
            'ilb-port': '$(ref.internal-lb.ilb-port)',
            'urlPath-namedPort': str(context.properties['urlPath-namedPort']),
            'network-cidr': context.properties['trust-subnet-cidr'],
        }
    }]
   
    host_project = context.properties['host-project'] 
    app_trust_vpc_project, trust_network = context.properties['trust-network'].split('/')
    if app_trust_vpc_project != host_project:
        resources.append({
            'name': "allow-peer-trust",
            'type': 'firewall.py',
            'properties': {
                'host_project':app_trust_vpc_project,
                'network': trust_network,
                'sourceRange': '0.0.0.0/0',
                'protocol': 'all',
                'ports': '',
            }
        })

    return {
        'resources': resources,
        'outputs': [
            {'name': 'ilb-ip', 'value': '$(ref.internal-lb.ilb-ip)'}, 
            {'name': 'ilb-port', 'value': '$(ref.internal-lb.ilb-port)'},
            {'name': 'urlPath-namedPort', 'value': str(context.properties['urlPath-namedPort'])}
        ]
    }
