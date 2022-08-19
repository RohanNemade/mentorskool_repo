# Importing the libraries
import requests
import json
import pandas as pd

# Defining the function that will generate pandas dataframe of all chracters with given starting letter.
def character_df_generator(api_key, hash, nameStartsWith):
    if(nameStartsWith == 0 or nameStartsWith == "0"):
        return "Starting letter cannot be 0"
    limit = 100
    ts = 1 # Hard coded for now.
    main_list = [] # The list where all the data for each charater would be stored as sub-lists.
    req_url = "http://gateway.marvel.com/v1/public/characters?ts=" + str(ts) + "&apikey=" + str(api_key) + "&hash=" + str(hash) + "&nameStartsWith=" + str(nameStartsWith)
    response = requests.get(req_url)
    response.raise_for_status()
    results = response.json()
    num_characters = results["data"]["total"]
    remaining = num_characters
    offset = 0
    while remaining > 0:
        req_url = "http://gateway.marvel.com/v1/public/characters?ts=" + str(ts) + "&apikey=" + str(api_key) + "&hash=" + str(hash) + "&nameStartsWith=" + str(nameStartsWith) + "&limit=" + str(limit) + "&offset=" + str(offset)
        response = requests.get(req_url)
        response.raise_for_status()
        result = response.json()
        remaining -= limit
        offset += limit
        temp = []
        for j in range(result["data"]["count"]):
        # Extracting specific data for each character.
            character_name = result["data"]["results"][j]["name"]
            num_event_appearences = result["data"]["results"][j]["events"]["available"]
            num_series_appearences = result["data"]["results"][j]["series"]["available"]
            num_stories_appearences = result["data"]["results"][j]["stories"]["available"]
            num_comics_appearences = result["data"]["results"][j]["comics"]["available"]
            character_id = result["data"]["results"][j]["id"]
            # Aggregating all data of each character in a list.
            temp = [character_name, num_event_appearences, num_series_appearences, num_stories_appearences, num_comics_appearences, character_id]
            main_list.append(temp)

    # Converting the main_list to pandas dataframe.
    return pd.DataFrame(main_list, columns=['character_name', 'num_event_appearences', 'num_series_appearences', 'num_stories_appearences','num_comics_appearences', 'character_id'])

# Testing
print(character_df_generator(api_key="3adcdda25a9e7db177a62197e5a87411", hash="1560178784bb76988a97d8f22a966494", nameStartsWith='b'))