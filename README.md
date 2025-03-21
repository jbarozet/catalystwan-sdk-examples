# Catalyst SD-WAN Python SDK Examples

catalystwan client is a package for creating simple and parallel automatic requests via Cisco Catalyst Manager API.
It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant).
The library is not dependent on environment which is being run in, you just need a connection to any vManage.

Architecture:
- Layer1: Core. provides basic functionality for interacting with vManage API. Provides a session object for interacting with vManage API.
- Layer2: Endpoints. provides high-level API for interacting with vManage API.
- Layer3: User APIs. provides user-friendly API for interacting with vManage API.

Check it out:

- <https://github.com/cisco-en-programmability/catalystwan-sdk>
- <https://pypi.org/project/catalystwan/>

This repository just gives a few examples of how to use catalystwan SDK.

## Installation

Create virtual environment:

```example
% python3 -m venv .venv
```

Activate virtual environment:

```example
% source .venv/bin/activate
(venv) %
```

Upgrade initial virtual environment packages:

```example
(venv) % pip install --upgrade pip setuptools
```

Install required Python packages:

```example
(venv) % pip install -r requirements.txt
```

## Usage

Make sure you have the below environment variables defined in `.env` file:

- vmanage_host
- vmanage_user
- vmanage_password

Use `export catalystwan_devel=true` if you want to have debug messsages.
They will be dumped into catalystwan.log file.

Python examples are organized as follows:

- `01-raw` folder: examples based on catalystwan layer1
- `02-endpoints` folder: examples based on catalystwan layer2, endpoints
- `03-api` folder: examples based on catalystwan layer3, user APIs
- `04-config-group` fodler: example of config-group and profiles definition
- `alarms` folder: examples of API usage for alarms.
- `devices` folder: examples of API usage for devices.
