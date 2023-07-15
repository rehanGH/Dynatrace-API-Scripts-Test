# Dynatrace API Host Monitoring Settings (Use it at your own risk, havent really tested it out too much)

### This code snippet demonstrates the use of the Dynatrace API to modify monitoring settings for hosts. Here's a breakdown of the code and its functionality: (Use it at your own risk)


## Importing Required Libraries
```python
import requests
import json
```

The code imports the necessary libraries for making HTTP requests (requests) and working with JSON data (json).


## Dynatrace API Endpoint and Credentials

```python
base_url = "https://<env>.live.dynatrace.com/api/v2/"
api_token = "dt0c01.XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

The base_url variable stores the base URL of the Dynatrace API endpoint. Replace <env> with the appropriate environment identifier. The api_token variable holds the API token required for authentication and authorization. Make sure to replace it with your valid token.

## Step 1: Get Object IDs for HOST Schema

```python
headers = {"Authorization": f"Api-Token {api_token}"}
params = {"schemaIds": "builtin:host.monitoring", "fields": "objectId,value,scope"} 
response = requests.get(base_url + "settings/objects", headers=headers, params=params)
host_objects = response.json()
```

This step retrieves all Object IDs associated with the HOST schema using a GET request to the Dynatrace API. The request includes the required headers and parameters. The response is stored as JSON in the host_objects variable.

## Extracting Host IDs and Object IDs

```python
host_ids = []
object_ids = []
for item in host_objects["items"]:
    host_ids.append(item["scope"])
    object_ids.append(item["objectId"])
```

The code iterates through the retrieved host_objects and extracts the host IDs and object IDs. These IDs will be used in subsequent steps.

## Step 2: Get Host Information

```python
hostname_mapping = {}
for host_id in host_ids:
    response = requests.get(base_url + f"entities/{host_id}", headers=headers, params={"fields": "managementZones,tags"})
    host_info = response.json()
    hostname = host_info.get("displayName")
    tags = host_info.get("tags", [])
    management_zones = host_info.get("managementZones", [])
    
    hostname_mapping[host_id] = {
        "hostname": hostname,
        "tags": tags,
        "managementZones": management_zones
    }
```

In this step, the code retrieves information about the hosts using their host IDs. It makes GET requests to the Dynatrace API, providing the required headers and parameters. The response contains the host's display name, tags, and management zones. This information is stored in the hostname_mapping dictionary using the host ID as the key.

## Step 3: Filter Hosts

```python
filtered_hosts = []
for host_id, host_data in hostname_mapping.items():
    hostname = host_data["hostname"]
    tags = host_data["tags"]
    management_zones = host_data["managementZones"]
    
    # Example filtering: only modify hosts with a specific tag value or in a specific management zone
    for tag in tags:
        if tag.get("context") == "EXAMPLE_KEY" and tag.get("key") == "EXAMPLE_VALUE":
            filtered_hosts.append(host_id)
            break
    
    # Uncomment the following lines if you want to filter based on management zones
    # for management_zone in management_zones:
    #     if management_zone.get("name") == "Test":
    #         filtered_hosts.append(host_id)
    #         break
```

This step demonstrates how to filter hosts based on specific criteria. The code iterates through the hostname_mapping dictionary, extracting the hostname, tags, and management zones for each host. In this example, it checks if the host has a specific tag value ("EXAMPLE_KEY": "EXAMPLE_VALUE"). If it matches, the host ID is added to the filtered_hosts list. You can uncomment and modify the code to filter based on management zones as well.

## Step 4: Modify Monitoring Settings

```python
payload = {
    "value": {
        "enabled": True,  # or False
        "autoInjection": True  # or False
    }
}

for host_id in filtered_hosts:
    object_id = object_ids[host_ids.index(host_id)]
    response = requests.put(base_url + f"settings/objects/{object_id}", headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Modified monitoring settings for host ID: {host_id} (Object ID: {object_id})")
    else:
        print(f"Failed to modify monitoring settings for host ID: {host_id} (Object ID: {object_id})")

```

In the final step, the code modifies the monitoring settings for the selected hosts. It creates a payload containing the desired monitoring settings (enabled and autoInjection). The code then iterates through the filtered_hosts list and sends a PUT request to the Dynatrace API for each host. The request updates the monitoring settings by providing the appropriate object ID and the payload in the request body. The response status code is checked to determine if the modification was successful or not, and a corresponding message is printed.

Please note that this code is a simplified example and may require modifications to fit your specific use case or Dynatrace environment.