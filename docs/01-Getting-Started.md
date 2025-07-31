# Getting Started

Cisco Catalyst SD-WAN Manager API can be categorized in the following categories.

- Administrative and management APIs - Includes user, group and tenant management, software maintenance, backup and restore, and container management.
- Alarm and event APIs - Includes the alarm and event notification configuration, and alarm, event, and audit log queries.
- Configuration - Includes feature template, device template, device policy, device certificate, device action, action status, device inventory, and so on.
- Device real-time monitoring - Includes real-time monitoring of devices, links, applications, systems, and so on.
- Device state, statistics bulk APIs - Includes device states, aggregated statistics, and bulk queries.
- Troubleshooting and utility - Includes HTTP status codes for errors and troubleshooting

The following sections provide examples of the preceding categories. See Reference for an OpenAPI 3.0 Cisco Catalyst SD-WAN Manager API definition.

## Base URI

Every API request will begin with the following Base URI.

```
https://<vmanage-server>:<port>/dataservice
```

## Authentication

Note: API request headers for GET/POST/PUT/DELETE are

- For Cisco Catalyst SD-WAN Manager pre-19.2 - session cookie (jsessionid)
- For Cisco Catalyst SD-WAN Manager post-19.2 - session cookie (jsessionid) and Token
