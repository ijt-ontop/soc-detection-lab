# Day 3 - Custom Brute-Force Detection

## Overview

For Day 3, I created a custom Wazuh rule to detect multiple failed Windows logon attempts against the same account.

Previously, I had been looking at individual failed logon events in Wazuh. This time I wanted Wazuh to correlate those events and generate a higher-level alert when several failures happened within a short period.

The rule was configured to detect 5 failed logons against the same account within 60 seconds.

---

## Checking the Existing Local Rules

Before adding anything, I opened the Wazuh `local_rules.xml` file to see what was already configured.

The file is located at:

```bash
/var/ossec/etc/rules/local_rules.xml
```

This is where I added my own custom detection rule.

![Local Rules Before Custom Rule](../../screenshots/day-03/Wazuh-Local-Rules-Before-Custom-Rule.png)

---

## Creating the Custom Rule

I created a new rule with the ID `100100`.

The rule looks for repeated matches of Wazuh rule `60122`, which was being generated for the Windows failed logon events I was testing.

I also used `targetUserName` so the failed attempts have to be against the same account.

```xml
<group name="windows,authentication,">

<rule id="100100" level="10" frequency="5" timeframe="60">
  <if_matched_sid>60122</if_matched_sid>
  <same_field>win.eventdata.targetUserName</same_field>
  <description>Multiple Windows failed logons detected for the same account</description>
  <mitre>
    <id>T1110</id>
  </mitre>
  <group>authentication_failed,brute_force,</group>
</rule>

</group>
```

The main parts of the rule are:

- `frequency="5"` - five matching events are required
- `timeframe="60"` - they need to happen within 60 seconds
- `if_matched_sid 60122` - watches for the failed logon alerts
- `same_field` - checks that the attempts are against the same username
- `level="10"` - creates a higher-level alert when the rule triggers
- `T1110` - maps the alert to MITRE ATT&CK Brute Force

![Custom Rule Configuration](../../screenshots/day-03/Wazuh-Custom-Rule-100100-Configuration.png)

---

## Generating Failed Logons

To test the rule, I went onto `SOC-ENDPOINT-01`, locked the Windows VM and deliberately entered the wrong password several times for the `socanalyst` account.

I then went back into Wazuh Threat Hunting and filtered for:

```text
rule.id: 60122
```

Wazuh showed the failed logon events being generated.

Five of the attempts happened within roughly 11 seconds, so they were well within the 60-second window configured in the custom rule.

![Failed Logon Threshold](../../screenshots/day-03/Wazuh-60122-Failed-Logon-Threshold.png)

---

## Custom Rule Triggered

After generating the failed logons, I searched for my custom rule:

```text
rule.id: 100100
```

The rule successfully triggered.

![Custom Brute Force Detection](../../screenshots/day-03/Wazuh-Custom-Brute-Force-Detection-100100.png)

The alert showed:

- Rule ID: `100100`
- Level: `10`
- Agent: `SOC-ENDPOINT-01`
- MITRE ID: `T1110`
- Technique: `Brute Force`

This confirmed that Wazuh had taken the separate failed logon events and correlated them into one brute-force detection.

---

## Looking at the Alert

I opened the alert to check the information Wazuh had recorded.

![Custom Brute Force Alert Details](../../screenshots/day-03/Wazuh-Custom-Brute-Force-Alert-Details.png)

The alert details showed:

```text
Rule ID:        100100
Rule Level:     10
Frequency:      5
MITRE ID:       T1110
MITRE Tactic:   Credential Access
MITRE Technique: Brute Force
```

The rule description was:

```text
Multiple Windows failed logons detected for the same account
```

This matched the activity I had generated on the Windows endpoint.

---

## What I Learned

This part of the lab helped me understand the difference between seeing individual security events and correlating multiple events into a useful detection.

A single failed password could just be a user entering their password incorrectly. Several failed attempts against the same account in a short period are more suspicious.

I also got some experience with:

- Creating custom Wazuh rules
- Editing `local_rules.xml`
- Testing and troubleshooting XML rules
- Using frequency and timeframe conditions
- Correlating events using the username
- Testing a detection by generating activity on the endpoint
- Investigating the resulting alert in Wazuh
- Mapping detections to MITRE ATT&CK

## Result

The custom rule worked as expected.

After five failed logons against the same Windows account within 60 seconds, Wazuh generated the custom Level 10 alert `100100` and mapped the activity to MITRE ATT&CK `T1110 - Brute Force`.
