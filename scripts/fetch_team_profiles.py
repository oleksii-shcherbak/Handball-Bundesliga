import json
import os
import requests
import time

# API key
api_key = "nmNsRET3p01hiSy9H8Ib91fnOguSeoKR1Ug5xJoC"

# Base URL for the API endpoint
base_url = "https://api.sportradar.com/handball/trial/v2/en/competitors/{}/profile.json"

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

def fetch_team_profile(team_id):
    """
    Fetches the profile for a given team ID.

    Args:
        team_id (str): The ID of the team to fetch the profile for.

    Returns:
        dict: The JSON response containing the team's profile.
    """
    url = base_url.format(team_id)
    print(f"Requesting data from {url}")
    try:
        response = make_request(url, api_key)
        return response
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        if e.response.status_code == 429:
            print(f"Rate limit reached. Please wait and try again later.")
        else:
            print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def save_progress(data, filepath):
    """
    Saves the provided data to the specified filepath as a JSON file.

    Args:
        data (dict or list): The data to be saved.
        filepath (str): The path to the file where data should be saved.
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# Path to the input file containing all season information
input_path = os.path.join('C:\\', 'Users', 'oleks', 'Projects', 'Handball-Bundesliga', 'data', 'processed', 'all_season_info.json')

with open(input_path, 'r') as f:
    all_season_info = json.load(f)

all_team_profiles = []
output_path = os.path.join('C:\\', 'Users', 'oleks', 'Projects', 'Handball-Bundesliga', 'data', 'processed', 'all_team_profiles.json')

# Extract unique team IDs from the season information
team_ids = set()
for season in all_season_info:
    for stage in season.get('stages', []):
        for group in stage.get('groups', []):
            for team in group.get('competitors', []):
                team_ids.add(team['id'])

try:
    # Iterate through each team ID and fetch the profile
    for team_id in team_ids:
        print(f"Fetching profile for team {team_id}...")
        profile = fetch_team_profile(team_id)
        if profile:
            all_team_profiles.append({
                'team_id': team_id,
                'profile': profile
            })
        save_progress(all_team_profiles, output_path)

        # Pause between requests to avoid hitting rate limits
        time.sleep(1)

    print(f"All team profiles data saved to {output_path}")
except Exception as e:
    save_progress(all_team_profiles, output_path)
    
    # Print any error that occurs during the request or file operation
    print(f"Error: {e}")
