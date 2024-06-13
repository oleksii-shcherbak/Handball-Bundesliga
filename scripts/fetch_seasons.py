import json
import os
import requests

# API key
api_key = "nmNsRET3p01hiSy9H8Ib91fnOguSeoKR1Ug5xJoC"

# Base URL for the API endpoint
base_url = "https://api.sportradar.com/handball/trial/v2/en/competitions/sr%3Acompetition%3A149/seasons.json"

def make_request(url, api_key):
    """
    Makes a GET request to the specified URL with the given API key.

    Args:
        url (str): The URL to send the request to.
        api_key (str): The API key for authentication.

    Returns:
        dict: The JSON response from the API.
    """
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(f"{url}?api_key={api_key}", headers=headers)
    response.raise_for_status()
    return response.json()

try:
    # Fetch data from the API
    data = make_request(base_url, api_key)
    
    # Define the path to save the fetched data
    output_path = os.path.join('data', 'processed', 'seasons.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the data to a JSON file
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to {output_path}")
except Exception as e:
    # Print any error that occurs during the request or file operation
    print(f"Error: {e}")
