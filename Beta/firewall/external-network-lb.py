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

    resources = []
    prefix = context.env['deployment']
    region = context.properties['region']
    forwardingrule_name = prefix + '-forwardingrule-' + region
    targetpool_name = prefix + '-target-pool-' + region
    healthcheck_name = prefix + '-hc-tcp-lb-' + context.properties['appName']

    healthcheck_properties = {
        'description': 'Health Check for the External TCP Load Balancer',
        'checkIntervalSec': 10,
        'timeoutSec': 5,
        'unhealthyThreshold': 3,
        'healthyThreshold': 2,
        'port': int(context.properties['backEndPort'])
       
    }

    healthcheck_object = {
        'name': healthcheck_name,
        'type': 'compute.v1.httpHealthCheck',
        'properties': healthcheck_properties
    }

    targetpool_object = {
        'name': targetpool_name,
        'type': 'compute.v1.targetPool',
        'properties': {
            'region': region,
            'healthChecks': ['$(ref.' + healthcheck_name + '.selfLink)']
        }
    }

    forwarding_rule_object = {
        'name': forwardingrule_name,
        'type': 'compute.v1.forwardingRule',
        'properties': {
            'region': region,
            'portRange': context.properties['forwarding-rule-port'],
            'target': '$(ref.' + targetpool_name + '.selfLink)'
        }
    }
    resources.append(healthcheck_object)
    resources.append(targetpool_object)
    resources.append(forwarding_rule_object)
    
    return { 'resources': resources }


