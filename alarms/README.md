# Alarms

## Mapping: alarm to severity

API Call:
- GET https://{{vmanage}}:{{port}}/dataservice/alarms/severitymappings

[Response example](alarms/examples/example_payload_alarms_mapping.json)

Gives a list of all alarms classified by category:
- Critical
- Major
- Medium
- Minor
- Info

Each entry has multiple fields, including these 2 fields:
- "key": "CPU_Usage",
- "value": "CPU Usage"

## Query fields

API Call:
- GET https://{{vmanage}}:{{port}}/dataservice/alarms/fields

[Response example](alarms/examples/example_payload_alarms_fields.json)


## Collecting alarms

- API call: POST dataservice/alarms (payload=query)
- Bulk API call: GET dataservice/data/device/statistics/alarm?startDate={{startDate}}&endDate={{endDate}}&timeZone={{timeZone}}&count={{count}}

[Response example](alarms/examples/example_payload_alarms_bulk.json)

You can filter your queries using either of three provided fields:
- rulename (ex: cpu-usage)
- rule_name_display (ex: CPU_Usage)
- type (ex: cpu-usage)

```json
[cut]
{
  "entry_time": 1736504318507,
  "uuid": "b1a4892c-52d0-4af2-971f-1b35580a43f7",
  "message": "System CPU usage is above 60%",
  "type": "cpu-usage",
  "component": "System",
  "severity": "Medium",
  "severity_number": 3,
  "devices": [
    {
      "system-ip": "100.0.0.1"
    }
  ],
  "active": true,
  "values": [
    {
      "system-ip": "100.0.0.1",
      "host-name": "Manager01",
      "cpu-status": "usage-notice"
    }
  ],
  "acknowledged": false,
  "cleared_by": "",
  "suppressed": false,
  "suppressed_by": "",
  "rulename": "cpu-usage",
  "rule_name_display": "CPU_Usage",
  "values_short_display": [
    {
      "host-name": "Manager01",
      "system-ip": "100.0.0.1",
      "cpu-status": "usage-notice"
    }
  ],
  "cleared_time": 0,
  "statcycletime": 1736504318507,
  "tenant": "default",
  "eventname": "cpu-usage",
  "receive_time": 1736504770484,
  "system_ip": "100.0.0.1",
  "host_name": "Manager01",
  "site_id": "",
  "update_time": 1736504869228
},
[cut]
```

## List of alarm_type

- alarm_type = "omp-state-change"
- alarm_type = "tloc_down"
- alarm_type = "cpu-usage"
- alarm_type = "system-reboot-issued",
- alarm_type = "control-vbond-state-change",
- alarm_type = "rootca-sync-failure"
- alarm_type = "security-root-cert-chain-installed",
- alarm_type = "disk-usage"
- alarm_type = "sla-violation"
