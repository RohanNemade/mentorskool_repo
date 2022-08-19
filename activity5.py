# Importing the libraries
import requests
import json
import pandas as pd
import sys

# Character_filter takes five arguments three of which are for generating the dataframe in character_df_generator function.
def character_filter(api_key, hash, nameStartsWith, filter_column_name, filter_condition):
    # Generating the dataframe.
    character_df = character_df_generator(api_key, hash, nameStartsWith)
    if(filter_column_name not in character_df.columns):
        return "Column name incorrect"
    # Filtering the dataframe rows based on the query formed from concatenating filter_column_name and filter_condition.
    #The below line uses pandas query function
    #filtered_df = character_df.query(str(filter_column_name) + str(filter_condition))

    # The below line uses lambda function
    filtered_df = character_df.loc[character_df[filter_column_name].apply(eval("lambda x:" + str(filter_condition)))]
    return filtered_df

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

if __name__ == "__main__":
    # Arguments passed in CLI will be stored in args.
    args = sys.argv[1:] # 1: because the first entry is the filename itself which is not needed.
    # If only 3 arguments are passed then the character_df_generator function will be called else the character_filter function is called
    if(len(args) == 3):
        print("Calling character_df_generator function")
        print(character_df_generator(*args))
    else:
        print("Calling character_filter function")
        print(character_filter(*args))
        
    