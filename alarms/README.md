# Alarms

## Get alarms components and event names

Returns components
- GET https://{{vmanage}}:{{port}}/dataservice/event/component/keyvalue
- [Response example](examples/example_payload_alarms_events_components.json)

Returns event names
- GET https://{{vmanage}}:{{port}}/dataservice/event/types/keyvalue
- [Response example](examples/example_payload_alarms_events_types.json)

## Get alarm to severity mapping

API Call:
- GET https://{{vmanage}}:{{port}}/dataservice/alarms/severitymappings
- [Response example](examples/example_payload_alarms_mapping.json)

Gives a list of all alarms classified by category:
- Critical
- Major
- Medium
- Minor
- Info

Each entry has multiple fields, including these 2 fields:
- "key": "CPU_Usage",
- "value": "CPU Usage"

## Query: Filter Alarms

You can filter your queries using either of three provided fields:
- rulename (ex: cpu-usage)
- rule_name_display (ex: CPU_Usage)
- type (ex: cpu-usage)
- severity (ex: Critical)

Get query fields:
- GET https://{{vmanage}}:{{port}}/dataservice/alarms/fields
- [Response example](examples/example_payload_alarms_fields.json)

Example of query payload:

```json
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "field": "entry_time",
        "operator": "last_n_days",
        "type": "date",
        "value": [
          "100"
        ]
      },
      {
        "field": "rule_name_display",
        "operator": "in",
        "type": "string",
        "value": [
          "CPU_Usage"
        ]
      }
    ]
  },
  "size": 10000
}
```

or

```json
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "field": "entry_time",
        "operator": "between",
        "type": "date",
        "value": ["2025-01-01T08:00:00", "2025-03-17T08:00:00"]
      },
      {
        "field": "rule_name_display",
        "operator": "in",
        "type": "string",
        "value": ["CPU_Usage"]
      }
    ]
  },
  "size": 10000
}
```

## Get Alarms

Returns alarms from SD-WAN Manager stats DB:
- POST dataservice/alarms (payload=query, see section above "Query: Filter Alarms")

Using Bulk API call:
- GET dataservice/data/device/statistics/alarm?startDate={{startDate}}&endDate={{endDate}}&timeZone={{timeZone}}&count={{count}}
- [Response example](examples/example_payload_alarms_bulk.json)

Example of response (one entry:

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
