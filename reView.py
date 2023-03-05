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
        print(filename)
        # Read the CSV file into a data frame
        file_path = os.path.join(datadir_path, filename)
        df = pd.read_csv(file_path)
        # Append the data frame to the list
        df_list.append(df)

# Concatenate all data frames in the list into a single data frame
combined_df = pd.concat(df_list, ignore_index=True)
# group by the column 'nameWell' and count the number of rows in each group
grouped = combined_df.groupby('nameWell').size()
#write the nameWell to a neo4j database
print (grouped)
driver = GraphDatabase.driver("neo4j://71da7f31.databases.neo4j.io:7687", auth=("neo4j", "aSFA8gQAv7DAllGUyQ6JpSRvZ6scBtnqIoLfS5n0t98"))

