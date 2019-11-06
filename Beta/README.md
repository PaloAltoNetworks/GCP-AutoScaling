# AutoScaling the VM-Series on Google Cloud Platform

The Google Cloud Platform Plugin for Panorama 2.0 Beta  helps you configure a connection from
Panorama to a GCP project and VMs deployed within it. You can use the web interface to
globally enable monitoring for a GCP project, configure VM monitoring for a GCP project, and
configure connections to VMs in autoscaling deployments. Once a connection
is established, the plugin can retrieve predefined or user-defined metadata (predefined
attributes, user-defined labels for VMs, and user-defined network tags as listed in Attributes,
Tags, and Labels).

## Topology
![alt text](/Beta/gcp_autoscaling.PNG?raw=true "Topology for the Auto Scaling VM-Series Firewalls on GCP Beta")

# Documentation
Use of this beta is recommended only for those users already familar with the Google Cloud Platform. 

The deployment guide can be found [here](
https://github.com/PaloAltoNetworks/GCP-AutoScaling/blob/master/Beta/Autoscaling-On-GCP.pdf)


# Support Policy
***Community-Supported aka Best Effort:***      
This CFT is released under an as-is, best effort, support policy. These scripts should be seen as community supported and Palo Alto Networks will contribute our expertise as and when possible. We do not provide technical support or help in using or troubleshooting the components of the project through our normal support options such as Palo Alto Networks support teams, or ASC (Authorized Support Centers) partners and backline support options. The underlying product used (the VM-Series firewall) by the scripts or templates are still supported, but the support is only for the product functionality and not for help in deploying or using the template or script itself. Unless explicitly tagged, all projects or work posted in our GitHub repository (at https://github.com/PaloAltoNetworks) or sites other than our official Downloads page on https://support.paloaltonetworks.com are provided under the best effort policy.