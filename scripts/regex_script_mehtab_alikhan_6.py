'''
This script:
- Extracts place names from news articles using a gazetteer
- Improves recall by using all alternative names in the gazetteer
- Filters articles to only include those written after 2023-10-07
- Counts place name mentions per month
- Saves output files:
    - regex_counts.tsv → monthly frequency counts of place names

'''
import re
import os
import pandas as pd


# Create a DataFrame so we can export it to a structured TSV format

def write_tsv(data, column_list, path):
    """converts a list of data into a tsv file.

    It takes three arguments:
        data (dict): the dictionary
        column_list (list): a list of column names
        path (str): the path to which the tsv file will be written
    """
    
    # Create a DataFrame from the dictionary data with the specified columns

    df = pd.DataFrame(data, columns=column_list)
    df.to_csv(path, sep="\t", index=False)



# Define the folder where the articles are located
folder = "../articles"  



# Load the gazetteer, which contains place names (asciiname) and their alternative spellings
# We will build regex patterns that match any of these variants
path = "../gazetteers/geonames_gaza_selection.tsv"
with open(path, encoding="utf-8") as file:
    data = file.read() #Read the entire file content

# Initialize an empty dictionary to hold regex patterns for each place name
patterns = {}

# Split the gazetteer data into rows and process each row
rows = data.split("\n")
for row in rows[1:]:  # Skip the header row
    columns = row.split("\t") # Split each row by tabs into columns
    if not columns[0]:
        continue #skip empty rows
    name = columns[0]
    alt_names = columns[3].split(",") if len(columns) > 3 else []
    all_names = [name] + alt_names

    # Join all name variants into a single regex pattern separated by "|"
    # Example: "Gaza|Gaza City|غزة" — re.escape ensures special characters don't break the regex

    regex_pattern = "|".join(re.escape(n.strip()) for n in all_names if n.strip())
    patterns[regex_pattern] = {"placename": name, "mentions": {}}
    

    

# Initialize the dictionary to store monthly mentions
mentions_per_month = {}

# Now count the number of mentions of each place name across all articles:
for filename in os.listdir(folder): #iterates through all files in the folder
    if filename.endswith(".txt"): #only process text file 
        date = filename[:10]  # assumes filename starts with YYYY-MM-DD
        if date < "2023-10-07": #skips pre-war articles 
            continue  # skip to the next article if the date is too early

        # Create the full file path for the article
        file_path = f"{folder}/{filename}"


    # load the article content into Python:
        with open(file_path, encoding="utf-8") as file:
            text = file.read() 
            month = filename[:7]  # extract the month from the filename 

#search for each place name pattern in the article
            for pattern in patterns:
                matches = re.findall(pattern, text, flags=re.IGNORECASE)# Find all matches (case sensitive)
                n_matches = len(matches) # Count the number of matches found

# If the pattern was found in the article, update the count for the corresponding month
                if n_matches > 0:
                    if month not in patterns[pattern]["mentions"]:
                        patterns[pattern]["mentions"][month] = 0
                    patterns[pattern]["mentions"][month] += n_matches


            # Update mentions_per_month for each place name
                if pattern not in mentions_per_month:
                    mentions_per_month[pattern] = {}
                if month not in mentions_per_month[pattern]:
                    mentions_per_month[pattern][month] = 0
                mentions_per_month[pattern][month] += n_matches


# Print the total frequency of each place name across all months
for pattern in patterns:
    total_count = sum(patterns[pattern]["mentions"].values()) #Sum all mentions for the pattern across all months
    if total_count >= 1:  # Only print the pattern if it has been mentioned at least once
       print(f"found {patterns[pattern]['placename']} {total_count} times")


# Flatten the nested dictionary into a list of key-value pairs for output
output_data = []
for pattern in patterns:
    placename = patterns[pattern]["placename"]
    for month in patterns[pattern]["mentions"]:
        count = patterns[pattern]["mentions"][month]  # Get the count for the specific place and month
        output_data.append((placename, month, count))# Append to output_data as a tuple (placename, month, count)

# Write the output data to the regex_counts.tsv file
columns = ["placename", "month", "count"] # Define the column names for the output file
tsv_filename = "../output/regex_counts.tsv" # Set the path for the output file
write_tsv(output_data, columns, tsv_filename) # Call the function to write the data to a TSV file

