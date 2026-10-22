
# SOC Detection Lab

A cybersecurity home lab focused on security monitoring, threat detection, log analysis and incident investigation using Wazuh SIEM.

## Overview

This repository documents my practical experience building and operating a Security Operations Centre (SOC) home lab.

The lab provides an isolated environment to generate controlled security activity, collect and analyse security logs, investigate suspicious behaviour and develop detection rules.

The work is organised into individual projects, with each project focusing on different areas of security monitoring and incident investigation.

## Objectives

- Build and maintain an isolated cybersecurity testing environment.
- Monitor and analyse Windows security events.
- Generate controlled suspicious activity for investigation.
- Identify suspicious behaviour using security logs.
- Investigate events using Wazuh SIEM and Windows Event Viewer.
- Develop and test custom detection rules.
- Document investigations, evidence and findings.
- Strengthen practical SOC analyst and threat detection skills.

## Lab Architecture

The lab is built using Oracle VirtualBox and consists of three virtual machines:

| System | Purpose | IP Address |
|---|---|---|
| Windows 11 Endpoint | Monitored system for security event collection | 192.168.50.10 |
| Kali Linux | Generating controlled security activity | 192.168.50.20 |
| Ubuntu Server | Hosting Wazuh SIEM | 192.168.50.30 |

All three virtual machines communicate through an isolated VirtualBox internal network named `SOC-LAB`.

### Security Monitoring

The Ubuntu Server hosts the Wazuh manager, indexer and dashboard.

The Windows 11 endpoint has the Wazuh agent installed, allowing security events to be forwarded to the Wazuh server for centralised monitoring and investigation.

Windows Event Viewer is also used to examine local security logs and compare them with events collected by Wazuh.

## Tools and Technologies

- **Wazuh SIEM** — Centralised security monitoring, log analysis and alert investigation.
- **Windows 11** — Endpoint monitoring and Windows security event analysis.
- **Windows Event Viewer** — Reviewing and validating security events.
- **Kali Linux** — Generating controlled security activity.
- **Ubuntu Server** — Hosting the Wazuh infrastructure.
- **Oracle VirtualBox** — Virtualisation and isolated lab networking.
- **PowerShell** — Windows administration, event generation and security testing.
- **Linux CLI** — Server administration and Wazuh configuration.

## Projects

### Project 1 — SOC Lab Setup and Security Monitoring

**Status: Completed**

Established the virtualised SOC environment and configured centralised security monitoring.

Key activities:

- Configured Windows 11, Kali Linux and Ubuntu Server virtual machines.
- Established an isolated internal network.
- Installed and configured the Wazuh SIEM infrastructure.
- Deployed and connected the Windows Wazuh agent.
- Enabled and investigated Windows security logging.
- Analysed authentication-related events, including Event IDs 4624, 4625 and 4740.
- Compared Windows Event Viewer records with Wazuh events.
- Documented configuration steps and collected evidence.

### Project 2 — Threat Detection and Investigation

**Status: In Progress**

Building on the existing SOC lab by configuring additional security monitoring capabilities and preparing custom detection rules in Wazuh.

Key activities:

- Reviewed Wazuh configuration for custom detection rules.
- Worked with the Wazuh server through the Linux command line.
- Began creating custom Wazuh detection rules.
- Started validating rule configuration to ensure it can be loaded correctly.
- Preparing the environment for controlled security testing and future investigations.

**Next Steps:**
- Complete custom detection rule configuration and validation.
- Generate controlled security activity to trigger detection rules.
- Collect and analyse the resulting security alerts.
- Investigate detected events and document findings.

## Planned Investigation Methodology

Security investigations within the lab are designed to follow a structured process:

1. **Generate Activity** — Produce controlled security events within the isolated lab.
2. **Collect Logs** — Capture events using Windows logging and the Wazuh agent.
3. **Identify Events** — Search and filter relevant security events in Wazuh.
4. **Investigate** — Examine event details, timestamps, accounts and related activity.
5. **Validate** — Compare findings with endpoint logs and expected test behaviour.
6. **Document** — Record evidence, investigation steps and conclusions.

## Project Documentation

Detailed setup instructions, investigations, screenshots and findings are documented within the repository.


## Project Documentation

Detailed setup instructions, testing procedures and findings are documented throughout the repository.

### Lab Infrastructure

- [Day 1 — Windows Endpoint Setup](documentation/lab-infrastructure/day-01-windows-endpoint-setup.md)
- [Day 2 — Kali Linux Attacker Setup](documentation/lab-infrastructure/day-02-kali-attacker-setup.md)
- [Day 3 — Wazuh SIEM Setup](documentation/lab-infrastructure/day-03-wazuh-siem-setup.md)

### Security Projects

Individual security projects are organised into separate folders containing investigation notes, screenshots and supporting evidence.


## Skills Developed

- SIEM monitoring and alert investigation
- Windows security event analysis
- Log filtering and correlation
- Authentication event investigation
- PowerShell security monitoring
- Custom detection rule development
- Incident investigation and evidence collection
- Virtual machine and network configuration
- Technical documentation

## Future Development

Planned improvements include:

- Completing and validating custom Wazuh detection rules.
- Expanding detection coverage across additional security events.
- Investigating more complex attack scenarios.
- Improving event correlation and detection accuracy.
- Developing additional SOC investigation projects.
