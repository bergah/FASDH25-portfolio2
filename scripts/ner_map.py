import pandas as pd
import plotly.express as px

# Load datasets (relative paths from scripts/ folder)
ner_counts_df = pd.read_csv("../output/ner_counts.tsv", sep="\t")
ner_gazetteer_df = pd.read_csv("../output/ner_gazetteer.tsv", sep="\t")

# Clean column names
ner_counts_df.columns = ner_counts_df.columns.str.strip()
ner_gazetteer_df.columns = ner_gazetteer_df.columns.str.strip()

# Merge datasets on 'name'
merged_df = pd.merge(ner_gazetteer_df, ner_counts_df, on="Place", how="inner")

# Rename columns 
merged_df.rename(columns={
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'Count': 'frequency'  # Assuming the count column is named 'count'
}, inplace=True)

# Convert coordinates to numeric
merged_df['latitude'] = pd.to_numeric(merged_df['latitude'], errors='coerce')
merged_df['longitude'] = pd.to_numeric(merged_df['longitude'], errors='coerce')

# Drop rows with missing lat/lon or frequency
merged_df = merged_df.dropna(subset=['latitude', 'longitude', 'frequency'])

# Plot map
fig = px.scatter_map(
    data_frame=merged_df,
    lat="latitude",
    lon="longitude",
    hover_name="Place",
    size="frequency",
    color="frequency",
    title="NER-extracted Places",
    zoom=5
)

# Set map style
fig.update_layout(map_style="open-street-map")

# Save outputs (relative paths from scripts/ folder)
fig.write_html("../output/ner_map.html")
fig.write_image("../map_images/ner_map.png")  # Requires kaleido installed
