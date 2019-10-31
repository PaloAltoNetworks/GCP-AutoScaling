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
    """Create sample web server application.
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """

    properties = context.properties
    prefix = context.env['deployment']
    resources = []
    igms = []

    for zone in properties['zones']:
        it_name = prefix + '-it-' + zone
        igm_name = prefix + '-igm-' + zone
        as_name = prefix + '-as-' + zone

        igms.append(igm_name + '.instanceGroup')

        resources.append({
            'name': it_name,
            'type': 'compute.v1.instanceTemplate',
            'properties': {
                'properties': {
                    'labels': {'app_template_version': context.properties['app-template-version']},
                    'zone': zone,
                    'machineType': context.properties['app-machine-type'],
                    'canIpForward': True,
                    #'noAddress': True,
                    'disks': [{
                        'deviceName': 'boot',
                        'type': 'PERSISTENT',
                        'boot': True,
                        'autoDelete': True,
                        'initializeParams': {
                            'sourceImage': 'https://www.googleapis.com/compute/v1/projects/click-to-deploy-images/global/images/lamp-v20190909'
                        }
                    }],
                    'metadata': {
                        'items': [
                            {'key': 'ssh-keys','value': context.properties['sshkey']},
                            {'key': 'serial-port-enable','value':'1'},
                            {'key': 'startup-script', 'value': ''.join(['#!/bin/bash\n',
                                                                        'sudo ln -sf /etc/apache2/conf-available/serve-cgi-bin.conf /etc/apache2/conf-enabled/serve-cgi-bin.conf\n',
                                                                        'sudo ln -sf /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load\n',
                                                                        'sudo mkdir -p /var/www/html/app1\n',
                                                                        'sudo cp /var/www/html/index.html /var/www/html/app1/index.html\n',
                                                                        "sudo sed  -i -e 's/Apache2 Debian Default Page/Apache2 APP1 Default Page/g' /var/www/html/app1/index.html\n",
                                                                        'sudo mkdir -p /var/www/html/app2\n',
                                                                        'sudo cp /var/www/html/index.html /var/www/html/app2/index.html\n',
                                                                        "sudo sed  -i -e 's/Apache2 Debian Default Page/Apache2 APP2 Default Page/g' /var/www/html/app1/index.html\n",
                                                                        'systemctl restart apache2\n'])}
                        ]
                    },
                    'tags': {
                        'items': [context.properties['app-instance-tag']]
                    },
                    #'serviceAccounts': [{
                        #'email': context.properties['service-account'],
                    #    'scopes': [
                    #        'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                    #        'https://www.googleapis.com/auth/devstorage.read_only',
                    #        'https://www.googleapis.com/auth/logging.write',
                    #        'https://www.googleapis.com/auth/monitoring.write',
                    #    ]}
                    #],
                    'networkInterfaces': [
                        {'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                                 context.properties['host-project'],'/global/',
                                 'networks/', context.properties['trust-network']]),
                        'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                                 context.properties['host-project'],'/regions/', context.properties['region'],
                                 '/subnetworks/', context.properties['trust-subnet']])
                        #'accessConfigs': [{
                        #    'name': 'External NAT',
                        #    'type': 'ONE_TO_ONE_NAT'}]
                        }
                    ]
                }
            }
        })

        resources.append({
            'name': igm_name,
            'type': 'compute.v1.instanceGroupManager',
            'properties': {
                'zone': zone,
                'targetSize': context.properties['size'],
                'baseInstanceName': prefix + '-' + zone,
                'instanceTemplate': '$(ref.' + it_name + '.selfLink)'
            }
        })

        resources.append({
            'name': as_name,
            'type': 'compute.v1.autoscaler',
            'properties': {
                'zone': zone,
                'target': '$(ref.' + igm_name + '.selfLink)',
                'autoscalingPolicy': {
                    'maxNumReplicas': context.properties['maxSize'],
                    'minNumReplicas': context.properties['minSize'],
                    'cpuUtilization': {
                        "utilizationTarget": context.properties['utilTarget']
                    },
                }
            }
        })

    return { 'resources': resources }

