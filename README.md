# FASDH25-portfolio2
A repository for students' portfolios for mini-project 2

# MINI-PROJECT-2

This project analyzes how often and where Gaza place names appear in news articles after October 7, 2023, using both regex + gazetteer and NER-based approaches. It extracts and counts location mentions, geocodes them, and visualizes the results through interactive maps. The workflow involves data filtering, entity recognition, normalization, and frequency mapping to trace media focus over time and space.

## **2A** Gaza Places Mentions in News Articles (Regex + Gazetteer Method)

This project analyzes how often different places in Gaza are mentioned in news articles after October 7, 2023. It uses a regex-based approach with a curated gazetteer of Gaza place names to detect mentions and generate monthly frequency statistics.

---
This README is designed to:
- Help understand the purpose and content of this project.
- Guide others on how to reproduce or build on this work.
- Explain the methods and choices made during the process.

---

### Objective

The goal is to extract mentions of Gaza place names from a collection of dated articles and count how often each location appears per month. This is achieved using regular expressions constructed from a gazetteer of known place names.

---

### Steps include

1. **Load and Parse Gazetteer**
   - Reads a TSV file containing standardized (`asciiname`) and alternative names for Gaza places.
   - Builds regex patterns to match all name variants.

2. **Filter Articles by Date**
   - Selects only those articles published after **October 7, 2023** using filename-based dates.

3. **Scan Text with Regex**
   - Reads each article and uses the regex patterns to find all mentions of places.
   - Matches are counted and grouped by month (`YYYY-MM`) and place name.

4. **Aggregate and Export**
   - Final counts are organized into a list of `[place, year-month, frequency]`.
   - Writes this data to a TSV file for further analysis or visualization.

---


## Output

The final TSV file (`output/regex_count.tsv`) contains three columns:

Asciiname Year-Month Frequency
Gaza City 2023-11 18
Rafah 2023-11 9
...

This format makes the data easy to visualize in charts or geographic maps.

---

## **2B** Gaza_Ner2_sahar_mehtab_atiya
### NER of place names of January 2024in Gaza War Coverage
This project uses stanza (NLP) to extract and analyze place names mentioned in articles about Gaza war. These used articles were published in January 2024. 

### Repository Structure
## Create a copy in google Colab and save as
----Gaza _Ner2_sahar_mehtab_atiya. ipynb
## Completing the Stanza NER pipeline
----data:
	/content/bergah/FASDH25-portfolio2/
## Output file with place names and their frequency counts
----ner_counts.tsv 
## This file
----README.md
  ABOUT PROJECT
The goal of this part of the project is to extract, clean, and count places mentioned in news articles written during January 2024 related to the Gaza war. 

## Google Colab is used to store and run input code and save output in .tsv file.
## Saving the notebook as Gaza_NER2_sahar_mehtab_atiya.ipynb.

### Step of segment of the project
#### setup and preprocessing 
_ The colab notebook is copied and renamed according to group members
_The portfolio Github repository is cloned into Colab
_The path is created

#### Filtering Articles by Data
_A function checks each article’s name for January 2024
_Only files from January 2024 are processed 

#### Named entity recognition with stanza
_ The stanza pipeline (tokenize, ner) is initialized.
_ Each file is passed through the pipeline, and only entities tagged as "GPE" (Geo-Political Entities) are retained.

#### Cleaning and Normalizing places names
_Possessive forms like “Gaza’s” are cleaned and merged with “Gaza.”
_Titles and casing are normalized using regex and string methods.
_All duplicate variations are merged into clean keys.

#### Exporting Results
	Cleaned place names and their frequency counts are written to a TSV file ner_counts.tsv.


## **3** NER Gazetteer Builder


### project discription
This project generated a Gazetteer file named NER_hazetteer.tsv in collab.


#### Details
 it conatians geographic coordinates (latitude and longitude) for place names which were identified through Named Entity Recognition (NER).
- ner_counts.tsv contains all the places names and its frequences.  
- it used ner_counts.tsv as a input file.
- geocoding was used to to retrieve coordinates automatically. 
- For any place names where coordinates could not be found, "NA" is recorded.
- Then manually added the coordinates of the places   which are recorded as NA.

### output
- Final output is a tsv file named 'NER_gazetteer.tsv'.
- it contains of three columns: 
- placename
- latitude 
- longitude




## **4A** Regex-Based Place Name Frequency Mapping


### Overview

-This step involves visualizing place names mentioned in Gaza-related news articles since October 7, 2023. 
-The place names were extracted using **regular expressions (regex)** and matched against a **gazetteer** (`geonames_gaza_selection.tsv`). 
-The frequency of these place names over time was mapped using **Plotly Express** on an animated, interactive map.

---

### Files Used

- **`../output/regex_count.tsv`**: A TSV file containing place names and their monthly frequencies extracted via regex.
- **`../gazetteers/geonames_gaza_selection.tsv`**: A curated gazetteer of place names in Gaza with corresponding latitude and longitude.
### Output files
- **`regex_map.py`**: The script that reads, merges, and maps the data.
- **`regex_map.html`** and **`regex_map.png`**: The final interactive map and its static image version.

---

### What the Script Does

1. **Reads the data**: Loads the regex frequency data and gazetteer coordinates.
2. **Merges the data**: Matches placenames to their geographic coordinates.
3. **Creates a map**: Uses `plotly.express.scatter_mapbox` to visualize place frequencies over time.
4. **Saves the output**: Creates and saves an interactive map (`regex_map.html`) and a static image (`regex_map.png`).

---

### Display Experiments and Final Choice

We tried multiple options for mapping the frequency data:

#### **Attempt 1: Static Map Without Time Animation**
- We initially tested a basic static map showing all place frequencies combined.
- Problem: It lacked the ability to show change over time, making it harder to analyze trends.

#### **Attempt 2: Choropleth Map**
- A choropleth (shaded region) map was considered, but it wasn't suitable because our data points are individual locations (not whole regions or administrative zones).

#### **Final Approach: Animated Scatter Map**
- We used `plotly.express.scatter_mapbox` with:
  - **Size and color** representing frequency.
  - **Animation frame** set to `Year-Month` for temporal visualization.
  - **OpenStreetMap** as the background map style.
- **Why this works best**:
  - It allows the user to observe **month-by-month changes** in place mentions.
  - Interactive hover tooltips show place names and help explore trends intuitively.
  - Size + color encode intensity of mentions, giving a clear visual hierarchy.

### Note:
We chose `scatter_mapbox` despite the deprecation warning, as it still supports animation frames, which is not yet fully available in the newer `scatter_map`. We documented this for future migration. 

---


Output Preview
regex_map.html: Interactive, animated map showing how often different Gaza locations were mentioned each month.

regex_map.png: Static image for reference or inclusion in printed material.
![regex map](https://github.com/bergah/FASDH25-portfolio2/blob/main/map_images/regex_map.png)




## **4B** NER-based Place Name Mapping (January 2024)

This project visualizes the frequencies of place names extracted using **Named Entity Recognition (NER)** from news articles, specifically for **January 2024**. The resulting interactive and static maps help to understand the geographic focus of the media coverage.

### Files Used

- `../output/ner_counts.tsv`:  
  A tab-separated file containing the frequency of each of extracted names for the month of January, 2024
  Key columns:
  - `name`: Place name
  - `count`

- `../output/NER_gazetteer.tsv`:  
  A tab-separated file containing geocoded coordinates (latitude and longitude) for each place name.  
  Key columns:
  - `asciiname`: Place name
  - `latitude`: Latitude coordinate
  - `longitude`: Longitude coordinate

### Output Files

- `../output/ner_map.html`:  
  An interactive Plotly map showing NER-extracted place names mentioned in January 2024.

- `../output/ner_map.png`:  
  A static PNG version of the same map for use in reports or offline settings.
![Ner map](https://github.com/bergah/FASDH25-portfolio2/blob/main/map_images/ner_map.png)

### How It Works

1. **Filter** the NER frequency data to keep only rows for **January 2024**.
2. **Rename columns** to make sure the frequency and coordinate data can be merged cleanly.
3. **Merge** the frequency data with the coordinates using the `placename`.
4. **Plot** the map using Plotly Express:
   - Bubble **size and color** reflect how frequently the place was mentioned.
   - **Hover labels** show the place name.
   - The map is styled using **OpenStreetMap** 


COMPARISONS
| Feature                   | **Regex-Based Map**                                                | **NER-Based Map**                                            |
| ------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------ |
| **Data Source**           | Extracted using hand-crafted regex patterns from a gazetteer       | Extracted using Stanza's pre-trained Named Entity Recognizer |
| **Place Name Coverage**   | Limited to predefined names in the gazetteer                       | Captures a broader, dynamic range of place names             |
| **Precision**             | High precision (only matches exact known names)                    | Moderate—some false positives due to generic GPE tagging     |
| **Recall**                | Lower—misses names not in the gazetteer or spelled differently     | Higher—detects unexpected or informal place mentions         |
| **Mention Cleaning**      | Built-in (standardized by regex construction)                      | Requires post-processing to merge variants (e.g. "Gaza’s")   |
| **Geocoding Reliability** | High—places are matched to exact coordinates via curated gazetteer | Varies—some places required manual coordinate completion     |
| **Map Detail & Focus**    | Fewer locations, more concentrated                                 | More varied mentions, sometimes noisy or redundant           |
| **Strength**              | Consistent and clean representation                                | Adaptive and rich in unexpected findings                     |
| **Weakness**              | Inflexible to new or misspelled place names                        | Less controlled, occasionally includes irrelevant GPEs       |



## Regex + Gazetteer
### Advantages:

- Easy to control and customize:
- we can define exactly what you're looking for. For example, if we want to find phone numbers, we can write a pattern like \d{10} and it will match exactly that.

- Faster and more efficient:
- Regex and gazetteers (lists of known names or keywords like cities, brands, etc.) are lightweight and quick to run. we can easily tweak regex patterns and add or remove entries in the gazetteer.

- No training required:
- Just write the rules, and they’ll work directly without needing any machine learning or labeled data.

- Great for specific, predictable data:
- Works very well for clearly structured information such as dates, codes, or names that follow a fixed format or come from a predefined list.

### Disadvantages:

- Rigid and brittle:
- If the format changes even slightly, regex can fail. For example, “March 5th” vs. “5 March” might not both be captured unless we write multiple patterns to account for all variations.

- Limited understanding of context:
- It cannot “understand” meaning — for instance, it might mistakenly identify “Apple” in “apple pie” as the company instead of the fruit.

## NER (Named Entity Recognition)
### Advantages:

- Understands context well:
- These models can distinguish between different meanings based on sentence context. For example, they can tell the difference between “Apple” as a fruit and “Apple” as a company.

- Handles variations better:
- Trained NER systems can recognize various ways people write names, places, or dates — even with some typos or new formats.

- More adaptable:
- Once trained, the model can manage a wide range of variations without needing constant rule updates.

- No need for manual rule updates:
- If the new data is similar to what the model has seen before, it can generalize and still perform well without redefining patterns.

### Disadvantages:

- Requires training data:
- To achieve good results, a labeled dataset is needed for training, which takes time and effort to prepare.

- Sensitive to noise:
NER models may struggle with misspellings, typos, or poorly formatted text (such as tweets or OCR-scanned documents).

- Slower than regex/gazetteer:
- Especially on large texts, NER can be more computationally expensive and slower to run.


## Self-Reflection

This project provides a solid foundation for understanding the frequency of place mentions using structured techniques. However, its heavy reliance on exact matches and a fixed gazetteer limits adaptability. With more time, incorporating machine learning-based entity recognition, disambiguation, and geocoding could greatly improve the system’s accuracy and usefulness.
With more time, we could improve accuracy by integrating fuzzy matching(something we learned online but very late), machine learning-based NER with domain-specific training, and automated disambiguation tools. Enhancing multilingual support and validating place references using contextual cues would also make the analysis more robust.

