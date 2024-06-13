import json
import os
from pymongo import MongoClient

# MongoDB Atlas connection string
mongo_uri = "mongodb+srv://oleksii-shcherbak:bXO47eMRgzC7Seg7@handball-bundesliga.egtujlx.mongodb.net/?retryWrites=true&w=majority&appName=Handball-Bundesliga"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client['Handball_Bundesliga']

# Load data from a JSON file
def load_json_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"The file {file_path} is empty.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from the file {file_path}: {str(e)}")

# Load data into a specified collection
def load_data_into_collection(data, collection_name):
    collection = db[collection_name]
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

# File paths to data
files = {
    "season_info": "C:/Users/oleks/Projects/Handball-Bundesliga/data/processed/all_season_info.json",
    "players": "C:/Users/oleks/Projects/Handball-Bundesliga/data/processed/all_season_players.json",
    "standings": "C:/Users/oleks/Projects/Handball-Bundesliga/data/processed/all_season_standings.json",
    "summaries": "C:/Users/oleks/Projects/Handball-Bundesliga/data/processed/all_season_summaries.json",
    "team_profiles": "C:/Users/oleks/Projects/Handball-Bundesliga/data/processed/all_team_profiles.json",
    "team_statistics": "C:/Users/oleks/Projects/Handball-Bundesliga/data/processed/all_team_statistics.json",
    "seasons": "C:/Users/oleks/Projects/Handball-Bundesliga/data/processed/seasons.json"
}

# Load and insert data into corresponding collections
for collection_name, file_path in files.items():
    try:
        data = load_json_file(file_path)
        load_data_into_collection(data, collection_name)
        print(f"Data from {file_path} successfully loaded into {collection_name} collection.")
    except Exception as e:
        print(f"Failed to load data from {file_path}: {str(e)}")

print("Data loading process completed.")
