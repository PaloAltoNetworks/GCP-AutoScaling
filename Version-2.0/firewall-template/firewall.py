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
    """Creates the firewall with environment variables.
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """
    prefix = context.env['deployment']
    firewall_name = prefix + '-' + context.env['name']
    if context.properties['network-exist']:
        network_ref = COMPUTE_URL_BASE + 'projects/' + context.env['project'] + '/global/' + 'networks/' + context.properties['network']
    else:
        network_ref = '$(ref.' + context.properties['network']+ '.selfLink)'
    if 'instance-tag' in context.properties:
        targetTags = [context.properties['instance-tag']]
    else:
        targetTags = []
    ports_s = context.properties['ports']
    resources = [{
        'name': firewall_name,
        'type': 'compute.v1.firewall',
        'properties': {
            'network': network_ref,
            'sourceRanges': context.properties['sourceRange'].split(','),
            'targetTags': targetTags,
            'allowed': [{
                'IPProtocol': context.properties['protocol'],
                'ports': ports_s.split(',') if ports_s != '' else []
            }]
        }
    }]
    return {'resources': resources}
