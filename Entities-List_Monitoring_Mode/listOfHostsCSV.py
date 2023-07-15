import csv
import requests

base_url = "https://<env>.live.dynatrace.com/api/v2"
api_token = "dt0c01.XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Replace with your actual API token

def get_hosts():
    entity_selector = 'type("HOST")'
    fields = 'properties.monitoringMode'
    params = {
        "entitySelector": entity_selector,
        "fields": fields
    }
    headers = {
        "Authorization": f"Api-Token {api_token}"
    }

    hosts = []
    next_page_key = None

    while True:
        if next_page_key:
            params["nextPageKey"] = next_page_key

        response = requests.get(f"{base_url}/entities", params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            entities = data["entities"]

            for entity in entities:
                host_id = entity["entityId"]
                display_name = entity["displayName"]
                monitoring_mode = entity["properties"]["monitoringMode"]
                hosts.append((host_id, display_name, monitoring_mode))

            next_page_key = data.get("nextPageKey")

            if not next_page_key:
                break

        else:
            print(f"Error occurred. Status code: {response.status_code}")
            break

    return hosts

def get_monitoring_modes(hosts):
    monitoring_modes = set()

    for host in hosts:
        _, _, monitoring_mode = host
        monitoring_modes.add(monitoring_mode)

    return monitoring_modes

hosts = get_hosts()
monitoring_modes = get_monitoring_modes(hosts)

# Save output to a CSV file
filename = "output.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Host ID", "Display Name", "Monitoring Mode"])  # Write header
    for host in hosts:
        host_id, display_name, monitoring_mode = host
        writer.writerow([host_id, display_name, monitoring_mode])

print(f"Output saved to {filename}")
