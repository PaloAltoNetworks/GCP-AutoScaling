# AutoScaling the VM-Series on Google Cloud Platform

The Panorama plugin for Google Cloud Platform (GCP) version 2.0 enables Panorama to manage VMSeries
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
![alt text](/Version-2.0/gcp_autoscaling.PNG?raw=true "Topology for the Auto Scaling VM-Series Firewalls on GCP")

# Documentation
Use of this generally available repository is recommended only for those users already familar with the Google Cloud Platform. 

The deployment guide can be found [here](
https://github.com/PaloAltoNetworks/GCP-AutoScaling/blob/master/Version-2.0/Autoscaling-On-GCP.pdf)

**Training Videos**   
- Firewall	***5:34***  [CLICK HERE](
https://github.com/PaloAltoNetworks/GCP-AutoScaling/tree/master/Version-2.0/Videos/GCP_AutoScale_Demo_Part1.mp4)    
- Application		***5:18***  [CLICK HERE](
https://github.com/PaloAltoNetworks/GCP-AutoScaling/tree/master/Version-2.0/Videos/GCP_AutoScale_Demo_Part2.mp4) 



# Support Policy
This release is now generally available. The firewall deployment templates are released under the official support policy of Palo Alto Networks through the support options that you've purchased, for example Premium Support, support teams, or ASC (Authorized Support Centers) partners and Premium Partner Support options. The support scope is restricted to troubleshooting for the stated/intended use cases and product versions specified in the project documentation and does not cover customization of the scripts or templates.

The application template is Community Supported.

Only projects explicitly tagged with "Supported" information are officially supported. Unless explicitly tagged, all projects or work posted in our GitHub repository or sites other than our official Downloads page are provided under the best effort policy..