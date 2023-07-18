import requests

# Replace with your Dynatrace environment URL
base_url = "https://<env>.live.dynatrace.com/api/v2"

# Replace with your Dynatrace API token
api_token = "dt0c01.XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Replace with your actual API token

# Define the headers with the API token
headers = {
    "Authorization": f"Api-Token {api_token}",
    "Content-Type": "application/json"
}

# Step 1: Get all token IDs
response = requests.get(f"{base_url}apiTokens", headers=headers)
response.raise_for_status()

# Extract token IDs from the response
token_ids = [token["id"] for token in response.json()["apiTokens"]]

# Get the current API token ID
current_token_id = "dt0c01.XXXXXXXXXXXXXXXXXXXXXXXX" 

# Step 2: Delete all tokens except the current one
for token_id in token_ids:
    if token_id == current_token_id:
        continue

    delete_url = f"{base_url}apiTokens/{token_id}"
    try:
        delete_response = requests.delete(delete_url, headers=headers)
        delete_response.raise_for_status()
        print(f"Deleted token with ID: {token_id}")
    except requests.exceptions.HTTPError as err:
        if delete_response.status_code == 404:
            print(f"Token with ID '{token_id}' not found. Skipping deletion.")
        else:
            raise err