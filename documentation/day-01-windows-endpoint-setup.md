# Day 1 - Windows Endpoint Setup

## What I did

On the first day of the project, I created the initial Windows endpoint that will be monitored throughout the project.

I used VirtualBox to create a Windows 11 Pro virtual machine and configured it with:

- 4 GB RAM
- 2 virtual processors
- 80 GB virtual storage
- Windows 11 Pro 64-bit

The VirtualBox VM was named `SOC-Windows-Endpoint` and the Windows device was named `SOC-ENDPOINT-01`.

## Network Configuration

I configured the Windows endpoint with two virtual network adapters.

### Adapter 1 - NAT

The first adapter uses NAT and provides the Windows VM with internet access. This allows the endpoint to download Windows updates and security tools without connecting the VM directly to my physical network.

### Adapter 2 - Internal Network

The second adapter is connected to an internal VirtualBox network named `SOC-LAB`.

This network will be used for communication between the machines within the cybersecurity lab, including the Windows endpoint, attacker machine and monitoring server.

Keeping this traffic on an internal network provides a controlled environment for generating and monitoring security activity.

## Evidence

Screenshots of the VM and network configuration are available in:

`screenshots/day-01/`
