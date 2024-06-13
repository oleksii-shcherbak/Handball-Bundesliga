import json
import os
import time
import requests

# API key
api_key = "nmNsRET3p01hiSy9H8Ib91fnOguSeoKR1Ug5xJoC"

# Base URL for the API endpoint
base_url = "https://api.sportradar.com/handball/trial/v2/en/seasons/{}/players.json"

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
    response = requests.get(f"{url}&api_key={api_key}", headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_all_players(season_id):
    """
    Fetches all players for a given season ID, handling pagination and avoiding duplicates.

    Args:
        season_id (str): The ID of the season to fetch players for.

    Returns:
        list: A list of players for the season.
    """
    start = 0
    limit = 200
    all_players = []
    unique_player_ids = set()
    request_count = 0

    while True:
        url = f"{base_url.format(season_id)}?start={start}&limit={limit}"
        print(f"Requesting data from {url}")
        try:
            response = make_request(url, api_key)
            if 'season_players' not in response:
                print(f"Unexpected response format: {response}")
                break
            players = response['season_players']
            if not players:
                print(f"No more players found for season {season_id}.")
                break

            new_players = []
            for player in players:
                player_id = player.get('id')
                if player_id and player_id not in unique_player_ids:
                    unique_player_ids.add(player_id)
                    new_players.append(player)
                else:
                    print(f"Duplicate or missing player ID: {player}")

            if not new_players:
                print(f"No new players found for season {season_id}.")
                break

            all_players.extend(new_players)
            start += limit
            request_count += 1

            # Pause between requests to avoid hitting rate limits
            time.sleep(1)

            # Print progress
            print(f"Request {request_count}: {len(new_players)} players")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  
                print(f"Rate limit reached. Please wait and try again later.")
                break
            else:
                print(f"HTTP error: {e}")
                break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    return all_players

def save_progress(data, filepath):
    """
    Saves the provided data to the specified filepath as a JSON file.

    Args:
        data (dict or list): The data to be saved.
        filepath (str): The path to the file where data should be saved.
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# Path to the input file containing season information
input_path = os.path.join('C:\\', 'Users', 'oleks', 'Projects', 'Handball-Bundesliga', 'data', 'processed', 'seasons.json')

with open(input_path, 'r') as f:
    all_season_info = json.load(f)

all_season_players = []
output_path = os.path.join('data', 'processed', 'all_season_players.json')

try:
    # Iterate through each season and fetch players
    for season in all_season_info['seasons']:
        season_id = season['id']
        print(f"Starting season {season_id}...")
        season_players = fetch_all_players(season_id)
        all_season_players.append({
            'season_id': season_id,
            'players': season_players
        })
        save_progress(all_season_players, output_path)
    
    print(f"All season players data saved to {output_path}")
except Exception as e:
    save_progress(all_season_players, output_path)
    # Print any error that occurs during the request or file operation
    print(f"Error: {e}")
