#Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#			http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def GenerateConfig(context):
	"""Create pubsub topic and subscription.
	Args:
		context: The context object provided by Deployment Manager.
	Returns:
		A config object for Deployment Manager (basically a dict with resources).
	"""

	name = context.env['name']
	project = context.env['project']
	properties = context.properties
	prefix = context.env['deployment'] + "-" + project
	resources = []

	topic_name = prefix + '-panorama-apps-deployment'
	sub_name = prefix + '-panorama-plugin-subscription'
	resources.append({
		'name': topic_name,
		'type': 'gcp-types/pubsub-v1:projects.topics',
		'properties': {'topic': topic_name}})
	resources.append({
		'name': sub_name,
		'type': 'gcp-types/pubsub-v1:projects.subscriptions',
		'properties': {'subscription': sub_name,
		'topic': '$(ref.' + topic_name + '.name)'}})
 
	return {'resources': resources,
		'outputs': [{
		'name': 'vm-series-fw-template-pubsub-topic',
		'value': '$(ref.' + topic_name + '.name)'}
		]}
