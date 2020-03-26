#Copyright 2016 Google Inc. All rights reserved.
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

import base64
import json

def GenerateConfig(context):
    """Publish msg when app deployment is created, updated or deleted.
    Args:
        context: The context object provided by Deployment Manager.
    Returns:
        A config object for Deployment Manager (basically a dict with resources).
    """

    name = context.env['name']
    prefix = context.env['deployment']
    resources = []
    #fw_template_topic = 'project/'+ context.env['project'] + '/topics/' + context.properties['vm-series-fw-template-topic']
    fw_template_topic = context.properties['vm-series-fw-template-topic']
    app_topic = prefix + '-pubsub-topic'
    forwardingrule_name = prefix + '-fr-' + context.properties['region']
    data = {
        'app-deployment-name': prefix,
        'host-project'       : context.properties['host-project'],
        'fw-deployment-name' : context.properties['fw-deployment-name'],
        'ilb-ip': context.properties['ilb-ip'],
        'ilb-port': context.properties['ilb-port'],
        'named-port': context.properties['urlPath-namedPort'],
        'network-cidr': context.properties['network-cidr'],
    }


    resources.append({
        'name': app_topic + '-publish-add',
        'action': 'gcp-types/pubsub-v1:pubsub.projects.topics.publish',
        'properties': {
            'messages': [{ 
                'data': base64.b64encode(json.dumps(data).encode('utf-8')), 
                'attributes': {'version': context.properties['app-template-version'], 
                               'topic': fw_template_topic,
                               'type': 'ADD-APP', 
                               'ilb-ip': context.properties['ilb-ip'],
                               'ilb-port': context.properties['ilb-port'],
                               'named-port': context.properties['urlPath-namedPort'],
                               'app-deployment-name': prefix,
                               'host-project': context.properties['host-project'],
                               'fw-deployment-name' : context.properties['fw-deployment-name'],
                               'network-cidr': context.properties['network-cidr'],
                               }
            }],
            'topic': fw_template_topic
        },
        'metadata': {
            'runtimePolicy': ['CREATE'],
        }
    })

    resources.append({
        'name': app_topic + '-publish-update',
        'action': 'gcp-types/pubsub-v1:pubsub.projects.topics.publish',
        'properties': {         
            'messages': [{      
                'data': base64.b64encode(json.dumps(data).encode('utf-8')),
                'attributes': {'version': context.properties['app-template-version'], 
                               'topic': fw_template_topic,
                               'type': 'UPDATE-APP', 
                               'ilb-ip': context.properties['ilb-ip'],
                               'ilb-port': context.properties['ilb-port'],
                               'named-port': context.properties['urlPath-namedPort'],
                               'app-deployment-name': prefix,
                               'host-project': context.properties['host-project'],
                               'fw-deployment-name' : context.properties['fw-deployment-name'],
                               'network-cidr': context.properties['network-cidr'],
                               }
            }],
            'topic': fw_template_topic
        },
        'metadata': {
            'runtimePolicy': ['UPDATE_ALWAYS'],
        }
    })

    resources.append({
        'name': app_topic + '-publish-del',
        'action': 'gcp-types/pubsub-v1:pubsub.projects.topics.publish',
        'properties': {
            'messages': [{
                'data': base64.b64encode(json.dumps(data).encode('utf-8')),
                'attributes': {'version': context.properties['app-template-version'], 
                               'topic': fw_template_topic,
                               'type': 'DEL-APP', 
                               'ilb-ip': context.properties['ilb-ip'],
                               'ilb-port': context.properties['ilb-port'],
                               'named-port': context.properties['urlPath-namedPort'],
                               'app-deployment-name': prefix,
                               'host-project': context.properties['host-project'],
                               'fw-deployment-name' : context.properties['fw-deployment-name'],
                               'network-cidr': context.properties['network-cidr'],

                              }
            }],
            'topic': fw_template_topic
        },
        'metadata': {
            'runtimePolicy': ['DELETE'],
        }
    })
           
    return {'resources': resources}
