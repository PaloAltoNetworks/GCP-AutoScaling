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

def GenerateConfig(context):
    """Build a HTTP external load balancer.
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """

    prefix = context.env['deployment']
    forwardingrule_name = prefix + '-forwardingrule-' + context.properties['region']

    resources = []
    backend_names = []
    path_rules = []
    for index, portName in enumerate(context.properties['urlPath-namedPort-maps']):
        healthcheck_name = prefix + '-hc-' + portName['appName']
        backend_names.append(prefix + '-backend-' + portName['appName'])

        resources.append({
            'name': healthcheck_name,
            'type': 'compute.v1.httpHealthCheck',
            'properties': {
                'port': portName['namedPort'],
                'requestPath': '/'
            }
        }) 
  
        backends = []
        for zone in context.properties['zones']:
            igm_name = prefix + '-igm-' + zone
            backends.append({
                'name': igm_name +'-be1',
                'group': '$(ref.' + igm_name + '.instanceGroup)'})
 
        resources.append({
            'name': backend_names[index],
            'type': 'compute.v1.backendService',
            'properties': {
                'port': portName['namedPort'],
                'protocol': 'HTTP',
                'portName': portName['appName'],
                'backends': backends,
                'healthChecks': ['$(ref.' + healthcheck_name + '.selfLink)'],
                'loadBalancingScheme': 'EXTERNAL',
                'region': context.properties['region'],
                "connectionDraining": {
                    "drainingTimeoutSec": context.properties['connection-draining-timeout'] 
                }
            }
        })
        path_rules.append({'paths':portName['urlMapPaths'],
                           'service':'$(ref.' + backend_names[index] + '.selfLink)'}) 

    resources.append({
        'name': prefix + '-ext-loadbalancer',
        'type': 'compute.v1.urlMap',
        'properties': {
            'defaultService': '$(ref.' + backend_names[0] + '.selfLink)',
            'hostRules': [{
                'hosts': ['*'],
                'pathMatcher': 'pathmap'
            }],
            'pathMatchers': [{
                'name': 'pathmap',
                'defaultService': '$(ref.' + backend_names[0] + '.selfLink)',
                'pathRules': path_rules
            }]
        }
    })

    if context.properties['ssl-certificate-url']:
        resources.append({
            'name': prefix + '-targetproxy',
            'type': 'compute.v1.targetHttpsProxy',
            'properties': {
                'urlMap': '$(ref.' + prefix + '-ext-loadbalancer.selfLink)',
                'sslCertificates':[context.properties['ssl-certificate-url']]
            }
        })
    else:
        resources.append({
            'name': prefix + '-targetproxy',
            'type': 'compute.v1.targetHttpProxy',
            'properties': {
                'urlMap': '$(ref.' + prefix + '-ext-loadbalancer.selfLink)',
            }
        })

    resources.append({
        'name': prefix + '-forwardingrule',
        'type': 'compute.v1.globalForwardingRule',
        'properties': {
            'IPProtocol': 'TCP',
            'portRange': context.properties['forwarding-rule-port'],
            'target': '$(ref.' + prefix + '-targetproxy.selfLink)'
        }
    })
        
    return { 'resources': resources }


