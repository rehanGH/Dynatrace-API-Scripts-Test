import requests
import json
import csv

# Dynatrace API base URL
base_url = "https://<env>.live.dynatrace.com/api/v2"

# Dynatrace API token
api_token = "dt0c01.XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Function to get the host ID for a given hostname
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

# Function to update the settings with host IDs
# Replace the `payload` with the payload of the Maintenance Window you are trying to modify
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

# Read hostnames from CSV file
def read_hostnames_from_csv(csv_file):
    hostnames = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) > 0:
                hostnames.append(row[0])
    return hostnames

# CSV file path
csv_file = "hostnames.csv"

# Get hostnames from CSV file
hostnames = read_hostnames_from_csv(csv_file)

# Get host IDs for all hostnames
host_ids = []
for hostname in hostnames:
    host_id = get_host_id(hostname)
    if host_id:
        host_ids.append(host_id)

# Update settings with host IDs
update_settings(host_ids)
