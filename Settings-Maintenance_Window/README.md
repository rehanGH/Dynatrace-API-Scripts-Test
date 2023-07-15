# Dynatrace API Script

### Note this API is just me testing things out and isnt really efficient if you want to affect the services and procceses associated with the hosts
### Better to use more concise rules and possibly leverage a tag as a filter that is shared by the entites you are creating a Maintenance Window

This script demonstrates how to update settings for a maintenance window using the Dynatrace API.

## Setup

1. Import the required libraries: `requests` and `json`.

```python
import requests
import json
```

2. Set the base URL for the Dynatrace API and the API token.

```python
base_url = "https://<env>.live.dynatrace.com/api/v2/"
api_token = "dt0c01.XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

3. Specify the list of hostnames.

```python
hostnames = ["hostname1", "hostname2"]
```

## Functions

### `get_host_id(hostname)`

This function retrieves the host ID for a given hostname.

```python
def get_host_id(hostname):
    url = f"{base_url}/entities"
    headers = {
        "Authorization": f"Api-Token {api_token}"
    }
    params = {
        "entitySelector": f"type(\"HOST\"),entityName.equals(\"{hostname}\")"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["totalCount"] > 0:
            return data["entities"][0]["entityId"]
    return None
```

### `update_settings(host_ids)`

Replace the `payload` with the payload of the Maintenance Winodw you are trying to modify
You can get the using the scheamaId `builtin:alerting.maintenance-window` in the /settings/objects GET endpoint

This function updates the settings for a maintenance window using the provided host IDs.

```python
def update_settings(host_ids):
    url = f"{base_url}/settings/objects/{{replace_with_objectID_of_MW}}"
    headers = {
        "Authorization": f"Api-Token {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "value": {
            "enabled": True,
            "generalProperties": {
                "name": "Testing API",
                "maintenanceType": "PLANNED",
                "suppression": "DETECT_PROBLEMS_AND_ALERT",
                "disableSyntheticMonitorExecution": False
            },
            "schedule": {
                "scheduleType": "ONCE",
                "onceRecurrence": {
                    "startTime": "2023-07-15T09:09:00",
                    "endTime": "2023-07-15T10:09:00",
                    "timeZone": "UTC"
                }
            },
            "filters": []
        }
    }
    for host_id in host_ids:
        payload["value"]["filters"].append({
            "entityId": host_id,
            "entityTags": [],
            "managementZones": []
        })
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Settings updated successfully.")
    else:
        print(f"Failed to update settings. Status code: {response.status_code}")
        print(response.text)
```

## Main Execution

1. Initialize an empty list to store the host IDs.

```python
host_ids = []
```

2. Iterate over each hostname, retrieve the host ID using the `get_host_id()` function, and add it to the `host_ids` list if it's not `None`.

```python
for hostname in hostnames:
    host_id = get_host_id(hostname)
    if host_id:
        host_ids.append(host_id)
```

3. Call the `update_settings()` function with the `host_ids` list to update the settings for the maintenance window.

```python
update_settings(host_ids)
```

Make sure to replace `<env>` in the `base_url` with the appropriate environment value, and `<replace_with_objectID_of_MW>` in the `update_settings()` function with the actual object ID of the maintenance window you want to modify.

That's it! This script demonstrates how to update settings for a maintenance window using the Dynatrace API.
