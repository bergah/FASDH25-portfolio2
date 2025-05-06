# Importing the required libraries
import pandas as pd                    # pandas is used for handling tabular data (like CSV or TSV files)
import plotly.express as px           # plotly.express is used for making interactive

# Load Frequency Data
# Reading the place frequency data (generated from regex extraction)
# This file contains how many times a place is mentioned in each month
freq_df = pd.read_csv("../output/regex_count.tsv", sep="\t")


# Load Coordinates 
# Reading the gazetteer data (list of places with their coordinates)
# This file helps us map place names to their geographic coordinates
coords_df = pd.read_csv("../gazetteers/geonames_gaza_selection.tsv", sep="\t")

# Rename Columns to Have a Common Merge Column
# The frequency data uses "Asciiname", and the coordinate data uses "asciiname"
# We rename both to the same name: "placename", so we can merge them
freq_df.rename(columns={"Asciiname": "placename"}, inplace=True)    # Rename in frequency dataframe
coords_df.rename(columns={"asciiname": "placename"}, inplace=True)  # Rename in coordinates dataframe

# Merge Frequency + Location
# Merging the two datasets based on the shared "placename" column
# This adds coordinates to each frequency record
merged_df = pd.merge(freq_df, coords_df, on="placename", how="inner")  # "inner" keeps only matching places


# Plot Interactive Map

# Creating a scatter plot on a map using plotly
# Each dot represents a place, its size/color shows frequency
# Animation shows changes across months
fig = px.scatter_mapbox(
    merged_df,                 # the full dataset we want to plot
    lat="latitude",            # column with latitude
    lon="longitude",           # column with longitude
    size="Frequency",          # bubble size = how frequently the place was mentioned
    color="Frequency",         # bubble color = frequency too (for visual impact)
    hover_name="placename",    # when you hover over a point, it shows the place name
    animation_frame="Year-Month",  # animate the map month-by-month
    size_max=25,                # max bubble size
    zoom=8,                    # initial zoom level
    title="Regex-extracted Place Frequencies Over Time",  # map title
    mapbox_style="open-street-map"  # free, open street base map
)


# Save the Map as HTML and PNG

# Save interactive version (user can click/hover)
fig.write_html("../output/regex_map.html")

# Save static image (PNG format, for reports or sharing)
fig.write_image("../map_images/regex_map.png")
