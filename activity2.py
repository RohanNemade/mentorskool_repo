# Importing the libraries
import requests
import json
import pandas as pd

# Setting values of parameters
ts = 1 # Hard coded for now
md5 = "1560178784bb76988a97d8f22a966494"
api_key = "3adcdda25a9e7db177a62197e5a87411"
limit = 100

# Creating a single array containing the ASCII values of all alphabets and digits except 0.
starting_letter_ascii = list(range(ord('a'),ord('z')+1))
starting_letter_ascii += list(range(ord('1'), ord('9')+1))
# starting_letter cannot be zero as it raises blank parameter error

main_list = [] # The list where all the data for each charater would be stored as sub-lists.
req_url = "http://gateway.marvel.com/v1/public/characters?ts=" + str(ts) + "&apikey=" + str(api_key) + "&hash=" + str(md5)
response = requests.get(req_url)
response.raise_for_status()
results = response.json()
num_characters = results["data"]["total"]
remaining = num_characters
offset = 0
for i in starting_letter_ascii:
    char = chr(i) #Converting ASCII value to characters.
    req_url = "http://gateway.marvel.com/v1/public/characters?ts=" + str(ts) + "&apikey=" + str(api_key) + "&hash=" + str(md5) + "&nameStartsWith=" + str(char)
    response = requests.get(req_url)
    response.raise_for_status()
    results = response.json()
    num_characters = results["data"]["total"]
    remaining = num_characters
    offset = 0
    while remaining > 0:
        req_url = "http://gateway.marvel.com/v1/public/characters?ts=" + str(ts) + "&apikey=" + str(api_key) + "&hash=" + str(md5) + "&nameStartsWith=" + str(char) + "&limit=" + str(limit) + "&offset=" + str(offset)
        response = requests.get(req_url)
        response.raise_for_status()
        results = response.json()
        remaining -= limit
        offset += limit
        temp = []
        for j in range(results["data"]["count"]):
        # Extracting specific data for each character.
            character_name = results["data"]["results"][j]["name"]
            num_event_appearences = results["data"]["results"][j]["events"]["available"]
            num_series_appearences = results["data"]["results"][j]["series"]["available"]
            num_stories_appearences = results["data"]["results"][j]["stories"]["available"]
            num_comics_appearences = results["data"]["results"][j]["comics"]["available"]
            character_id = results["data"]["results"][j]["id"]
            # Aggregating all data of each character in a list.
            temp = [character_name, num_event_appearences, num_series_appearences, num_stories_appearences, num_comics_appearences, character_id]
            main_list.append(temp)

# Converting the main_list to pandas dataframe.
output_df = pd.DataFrame(main_list, columns=['character_name', 'num_event_appearences', 'num_series_appearences', 'num_stories_appearences','num_comics_appearences', 'character_id'])

print(len(output_df))
print(output_df.head())

