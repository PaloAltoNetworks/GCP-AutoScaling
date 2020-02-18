# AutoScaling the VM-Series on Google Cloud Platform

The Panorama plugin for Google Cloud Platform (GCP) version 2.0 Beta enables Panorama to manage VMSeries
firewalls securing VM monitoring and auto scaling deployments in GCP.

This topic focuses on an auto scaling use case that requires Google shared VPC technology to create a
common VPC network composed of a host project containing shared VPC networks and the VM-Series
firewalls, and a service project containing a sample application deployment. Palo Alto networks supplies
templates to help you deploy the VM-Series firewalls in the host project and deploy the sample application
in the service project.

Using Panorama to maintain your GCP managed instance groups has the following benefits:
- BYOL licenses can be used for the VM-Series firewalls.
- Panorama automatically monitors the VM-Series firewall status and automatically deregisters a VMSeries
firewall when it is automatically removed.
- With Panorama, you can create application enablement policies that protect and control the network.
Using Panorama for centralized policy and firewall management increases operational efficiency in
managing and maintaining a distributed network of firewalls.


## Topology
![alt text](/Beta/gcp_autoscaling.PNG?raw=true "Topology for the Auto Scaling VM-Series Firewalls on GCP Beta")

# Documentation
Use of this beta is recommended only for those users already familar with the Google Cloud Platform. 

The deployment guide can be found [here](
https://github.com/PaloAltoNetworks/GCP-AutoScaling/blob/master/Beta/Autoscaling-On-GCP.pdf)

**Training Videos**   
- Firewall	***5:34***  [CLICK HERE](
https://github.com/PaloAltoNetworks/GCP-AutoScaling/tree/master/Beta/Videos/GCP_AutoScale_Demo_Part1.mp4)    
- Application		***5:18***  [CLICK HERE](
https://github.com/PaloAltoNetworks/GCP-AutoScaling/tree/master/Beta/Videos/GCP_AutoScale_Demo_Part2.mp4) 



# Support Policy
***Community-Supported aka Best Effort:***      
This CFT is released under an as-is, best effort, support policy. These scripts should be seen as community supported and Palo Alto Networks will contribute our expertise as and when possible. We do not provide technical support or help in using or troubleshooting the components of the project through our normal support options such as Palo Alto Networks support teams, or ASC (Authorized Support Centers) partners and backline support options. The underlying product used (the VM-Series firewall) by the scripts or templates are still supported, but the support is only for the product functionality and not for help in deploying or using the template or script itself. Unless explicitly tagged, all projects or work posted in our GitHub repository (at https://github.com/PaloAltoNetworks) or sites other than our official Downloads page on https://support.paloaltonetworks.com are provided under the best effort policy.