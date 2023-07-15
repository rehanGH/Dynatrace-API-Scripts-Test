import requests
import json

# Dynatrace API endpoint and credentials
base_url = "https://<env>.live.dynatrace.com/api/v2/"

# Required scopes: settings.read, settings.write, and entities.read
api_token = "dt0c01.XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Step 1: Get all Object Ids for HOST schema
headers = {"Authorization": f"Api-Token {api_token}"}
params = {"schemaIds": "builtin:host.monitoring", "fields": "objectId,value,scope"} 
response = requests.get(base_url + "settings/objects", headers=headers, params=params)
host_objects = response.json()

if "error" in host_objects:
    print(f"Error occurred: {host_objects['error']['message']}")
    exit(1)

# Extracting host IDs and object IDs from the response
host_ids = []
object_ids = []
for item in host_objects["items"]:
    host_ids.append(item["scope"])
    object_ids.append(item["objectId"])

# Step 2: Get hostnames, tags, and management zones for the associated host IDs
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

# Step 3: Filter hosts based on specific criteria
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

# Step 4: Modify monitoring settings for the selected hosts
payload = {
    "value": {
        "enabled": True, # or False
        "autoInjection": True # or False
    }
}

for host_id in filtered_hosts:
    object_id = object_ids[host_ids.index(host_id)]
    response = requests.put(base_url + f"settings/objects/{object_id}", headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Modified monitoring settings for host ID: {host_id} (Object ID: {object_id})")
    else:
        print(f"Failed to modify monitoring settings for host ID: {host_id} (Object ID: {object_id})")
