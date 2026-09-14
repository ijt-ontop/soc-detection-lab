# Day 2 - Kali Attacker Setup

## What I did

For the second stage of the lab, I set up a Kali Linux virtual machine (VM) that will be used as the attacker machine later in the project.

I downloaded the official pre-built Kali Linux VirtualBox image and imported it into VirtualBox. I then renamed the VM to `SOC-Kali-Attacker`.

The VM was configured with:

- 2 GB RAM
- 2 virtual processors
- 80 GB virtual storage
- Kali Linux 64-bit

## Network Configuration

I configured the Kali VM with two network adapters.

### Adapter 1 - NAT

I kept the first adapter as NAT so that Kali can still access the internet when I need to download updates or tools.

### Adapter 2 - SOC-LAB

The second adapter is connected to the internal VirtualBox network called `SOC-LAB`.

I used a separate adapter for this because I wanted the Kali and Windows VMs to communicate through the lab network rather than my normal home network.

The IP addresses I configured for the lab are:

- Windows endpoint: `192.168.50.10/24`
- Kali attacker: `192.168.50.20/24`

I didn't configure a gateway or DNS server on the `SOC-LAB` interface because the NAT adapter already handles internet access.

I first assigned `192.168.50.20/24` to Kali's `eth1` interface and then configured it through NetworkManager so the address would remain after a restart.

After restarting Kali, I checked `eth1` again and confirmed that the address was still there.

## Testing Connectivity

After setting up the network, I tested whether Kali could communicate with the Windows endpoint using:

`ping -c 4 192.168.50.10`

My first test failed with 100% packet loss.

I checked the Windows Firewall settings and found that the Windows endpoint was not allowing the ICMP echo requests.

Instead of turning the firewall off, I created a new inbound rule called:

`SOC-LAB - Allow ICMPv4 Echo Requests`

I configured the rule to allow ICMPv4 Echo Requests and restricted the remote IP addresses to:

`192.168.50.0/24`

I did this so the rule only applies to machines on my lab network rather than allowing the traffic from any network.

After adding the rule, I ran the ping again. This time I received 4 replies from the Windows endpoint with 0% packet loss.

I restarted Kali once more and tested the connection again to make sure both the IP configuration and connectivity still worked after a reboot.

## Snapshots

Once everything was working, I created new VirtualBox snapshots of the configured VMs.

I now have restore points that I can go back to if something goes wrong when I start making more changes to the lab.

## What I learned

This setup helped me understand how the two network adapters have different purposes within the lab.

The NAT adapter gives the VM internet access, while `SOC-LAB` is used for traffic between the machines inside the lab.

I also gained experience troubleshooting the connection between Kali and Windows. The initial ping was being blocked by Windows Firewall, and I resolved this by creating a specific inbound rule rather than disabling the firewall completely.

## Evidence

Screenshots from this stage are available here:

[screenshots/day-02/](../screenshots/day-02/)
