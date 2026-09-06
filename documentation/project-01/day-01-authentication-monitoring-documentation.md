# Project 1 - Windows Security Log Investigation

## Day 1 - Authentication Monitoring

### Overview

For the first part of this project, I generated controlled authentication activity on my Windows endpoint and investigated how the events appeared in both Windows Event Viewer and Wazuh.

The aim was to follow failed logon attempts through to an account lockout and then confirm that a successful logon was also detected after the account was restored.

The activity was generated on `SOC-ENDPOINT-01` and monitored through the Wazuh server running in my home lab.

---

## Failed Logon Attempts

I generated several failed logon attempts against the `socanalyst` account.

Windows recorded the failed attempts in the Security log as Event ID `4625`.

![Failed logon events in Windows Event Viewer](../screenshots/project-01/day-01/Event-Viewer-Failed-Logons-4625.png)

I then searched for the authentication failures in Wazuh Threat Hunting.

The repeated failures appeared against `SOC-ENDPOINT-01` with:

- Wazuh Rule ID: `60122`
- Rule Level: `5`
- Description: `Logon Failure - Unknown user or bad password`

![Repeated failed logons detected in Wazuh](../screenshots/project-01/day-01/Wazuh-Repeated-Failed-Logons.png)

This confirmed that the Windows authentication failures were being collected by Wazuh and could be investigated from the SIEM.

---

## Account Lockout

After several failed authentication attempts, the `socanalyst` account became locked.

Windows recorded this as Event ID `4740` - `A user account was locked out`.

![Windows account lockout event](../screenshots/project-01/day-01/Event-4740-Account-Lockout.png)

I searched for the same activity in Wazuh and found an account lockout alert.

Wazuh classified the event as:

- Wazuh Rule ID: `60115`
- Rule Level: `9`
- Description: `User account locked out (multiple login errors)`

![Account lockout detected in Wazuh](../screenshots/project-01/day-01/Wazuh-4740-Account-Lockout.png)

The increase from Level 5 failed-logon alerts to a Level 9 account-lockout alert made the lockout stand out as the more significant event during the investigation.

---

## Successful Logon

After restoring the account, I performed a successful logon using the `socanalyst` account.

Wazuh recorded the successful authentication as:

- Windows Event ID: `4624`
- Wazuh Rule ID: `60118`
- Rule Level: `3`
- Description: `Windows Workstation Logon Success`

![Successful Windows logon detected in Wazuh](../screenshots/project-01/day-01/Wazuh-4624-Successful-Logon.png)

---

## Day 1 Findings

The authentication activity produced a clear sequence of security events:

`Failed logons (4625) → Account lockout (4740) → Account restored → Successful logon (4624)`

I was able to identify the events locally in Windows Event Viewer and investigate the corresponding alerts from the Wazuh dashboard.

This gave me a starting point for the next stage of the project, where I investigated the underlying event fields and correlated Wazuh alerts with the original Windows Security logs.
