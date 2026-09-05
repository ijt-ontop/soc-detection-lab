# soc-detection-lab
A home lab to practise and strengthen security monitoring, threat detection and incident investigation skills.

## Overview

This project is a home built cybersecurity lab that I am using to develop practical experience.
The lab will be used to generate and analyse security events in a controlled environment using virtual machines. 
This project will allow me to practise working with logs, detecting suspicious activity and investigating security incidents. 

## Objectives

- Build an isolated environment for testing and experimenting
- Monitor Windows security events and logs
- Generate controlled suspicious activity 
- Identify and investigate security events
- Develop hands on practical experience using security monitoring tools
- Document my findings and investigations
  
## Lab Architecture

The lab is built using VirtualBox and currently contains three virtual machines:

- Windows 11 endpoint used as the monitored system
- Kali Linux machine used to generate controlled security activity
- Ubuntu Server running Wazuh for security monitoring and log analysis

The machines communicate through an isolated VirtualBox internal network called `SOC-LAB`.

| System           | IP Address |

| Windows Endpoint | 192.168.50.10 |
| Kali Linux       | 192.168.50.20 |
| Wazuh Server     | 192.168.50.30 |

## Current Setup

The Windows endpoint has been connected to Wazuh using the Wazuh agent. Events generated on the endpoint are collected by the Wazuh server and can be investigated through the Wazuh dashboard.

The Wazuh manager, indexer and dashboard are running on a dedicated Ubuntu Server virtual machine.

## Project Documentation

Detailed setup, testing and investigation notes are documented throughout the project.

- [Windows Endpoint Setup](documentation/day-01-windows-endpoint-setup.md)
- [Wazuh SIEM Setup and Endpoint Integration](documentation/day-03-wazuh-siem-setup.md)
