'''
This script:
- Extracts place names from news articles using a gazetteer
- Improves recall by using all alternative names in the gazetteer
- Filters articles to only include those written after 2023-10-07
- Counts place name mentions per month
- Saves output files:
    - regex_counts.tsv → monthly frequency counts of place names

'''

# Have to import important libraries

# Import the 're'for using regular expressions to search for place names
import re

# Import the 'os' to work with files and folders in the system
import os

# Import 'pandas' to handle data in table format and write output as TSV
import pandas as pd

# Define a function to write a list of data into a TSV (Tab-Separated Values) file
# Parameters: 
# - data: a list of lists, where each inner list is a row
# - column_list: a list of column headers
# - path: file path where the TSV will be saved
def write_tsv(data, column_list, path):
    df = pd.DataFrame(data, columns=column_list)  # Convert the list into a pandas DataFrame
    df.to_csv(path, sep="\t", index=False)        # Write the DataFrame to a TSV file without row numbers

# Specify the folder where the article files are stored
folder = "../articles"  

# Define the cutoff date; only articles after this date will be included
cutoff = "2023-10-07"  

# Specify the path to the gazetteer file containing place names and their alternate names
path = "../gazetteers/geonames_gaza_selection.tsv"

# Open and read the gazetteer file
with open(path, encoding="utf-8") as file:
    data = file.read()

# Initialize an empty dictionary to store regex patterns (keys) and their main place names (values)
patterns = {}

# Split the gazetteer file into rows (one per line), and remove any extra whitespace
rows = data.strip().split("\n")

# Extract the header row to get the column names
header = rows[0].split("\t")

# Get the column number (index) for 'asciiname' and 'alternatenames'
asciiname_idx = header.index("asciiname")
alternatenames_idx = header.index("alternatenames")

# Loop over each row (skipping the header) to extract place names
for row in rows[1:]:
    columns = row.split("\t")
    
    # Skip rows that are missing required columns
    if len(columns) <= max(asciiname_idx, alternatenames_idx):
        continue

    # Extract the main place name
    asciiname = columns[asciiname_idx].strip()

    # Extract alternative names (if any)
    alternatenames = columns[alternatenames_idx].strip()

    # Create a list of all name variants, starting with the main name
    all_names = [asciiname]

    # If alternate names are provided, add them to the list after stripping whitespace
    if alternatenames:
        all_names += [name.strip() for name in alternatenames.split(",") if name.strip()]

    # Join all name variants into a single regex pattern using OR (|), escaping special characters
    regex_pattern = r"|".join([re.escape(name) for name in all_names])

    # Store the regex pattern and map it to the main place name
    patterns[regex_pattern] = asciiname

# Initialize a dictionary to store monthly counts of place mentions
monthly_counts = {}

# Initialize a dictionary to store total mentions of each place, grouped by month
place_counts = {}

# Loop through all files in the articles folder
for filename in os.listdir(folder):

    # Extract the date from the filename (assuming the first 10 characters are the date)
    file_date = filename[:10]

    # Skip files dated on or before the cutoff
    if file_date <= cutoff:
        continue

    # Extract the year and month from the file name for grouping (e.g., "2023-11")
    year_month = file_date[:7]

    # Build the full path to the file
    file_path = f"{folder}/{filename}"

    # Open and read the contents of the article
    with open(file_path, encoding="utf-8") as file:
        text = file.read()

    # Initialize monthly counts for this year-month if not already done
    if year_month not in monthly_counts:
        monthly_counts[year_month] = {}

    # Loop through all regex patterns and associated main place names
    for pattern, place_name in patterns.items():
        # Find all matches of the pattern in the text (case-insensitive)
        matches = re.findall(pattern, text, re.IGNORECASE)

        # Count the number of matches found
        n_matches = len(matches)

        # Initialize the place name count for the current month if needed
        if place_name not in monthly_counts[year_month]:
            monthly_counts[year_month][place_name] = 0

        # Add the number of matches to the place's count for this month
        monthly_counts[year_month][place_name] += n_matches

# Loop through the monthly counts and collect non-zero mentions for each place
for year_month, counts in monthly_counts.items():
    for place, count in counts.items():
        if count > 0:
            # If the place hasn't been added to the result dictionary, initialize it
            if place not in place_counts:
                place_counts[place] = []

            # Add the month and frequency to the place's list of mentions
            place_counts[place].append([year_month, count])

            # Print a message showing the number of times the place was mentioned
            print(f"The place {place} was mentioned {count} times in {year_month}.")

# Prepare the data for TSV output by creating a list of rows (place, month, frequency)
output_data = []
for place, counts in place_counts.items():
    for count_info in counts:
        output_data.append([place, count_info[0], count_info[1]])

# Define the column headers for the TSV output
columns = ["Asciiname", "Year-Month", "Frequency"]

# Define the file path where the output will be saved
tsv_filename = "../output/regex_count.tsv"

# Call the function to write the data to a TSV file
write_tsv(output_data, columns, tsv_filename)

# Print a confirmation message
print("Monthly frequency counts saved in", tsv_filename)
