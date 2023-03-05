import os
import pandas as pd
from neo4j import GraphDatabase
# Define the path to the subdirectory
datadir_path = '/Users/jeff/Library/Mobile Documents/com~apple~CloudDocs/reView/reView/Equinor/'

# Create an empty list to hold the data frames for each file
df_list = []

# Loop through all files in the subdirectory
for filename in os.listdir(datadir_path):
    # Check if the file is a CSV file
    if filename.endswith('.csv'):
        # Read the CSV file into a data frame
        file_path = os.path.join(datadir_path, filename)
        df = pd.read_csv(file_path)
        # Append the data frame to the list
        df_list.append(df)
# Concatenate all data frames in the list into a single data frame
combined_df = pd.concat(df_list, ignore_index=True)
# for every row in the dataframe, print the value of the column 'nameWell'  
for index, row in combined_df.iterrows():
    print("MERGE (w:Well {name: '" + row['nameWell'] + "'})")
    print("MERGE (c:comment {name: '" + row['comments'] + "'})")


