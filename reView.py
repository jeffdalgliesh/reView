import os
import pandas as pd
from neo4j import GraphDatabase
# Define the path to the subdirectory
datadir_path = '/Users/jeff/Library/Mobile Documents/com~apple~CloudDocs/reView/reView/smallEquinor'
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
#loop through the dat frames and strip out all of the ' and " charagters and replace them with ''' and """ respectively 
# this is to prevent errors when writing the script to a text file
query = ""
# write the combined data frame to neo4j
# Define the connection string
uri = "neo4j+s://71da7f31.databases.neo4j.io"
# Define the user name and password
user = "neo4j"
password = "aSFA8gQAv7DAllGUyQ6JpSRvZ6scBtnqIoLfS5n0t98"
# Create a driver object
driver = GraphDatabase.driver(uri, auth=(user, password))
# Create a session object
session = driver.session()
# Delete all nodes and relationships in the graph
query = "MATCH (n) DETACH DELETE n;"
result = session.run(query)
#Loop through the data frame and write the data to neo4j
for index, row in combined_df.iterrows():
    combined_df.at[index, 'comments'] = str(row['comments']).replace("'", "''").replace('"', '""')
    #replace all of the non-ascii characters with a space
    combined_df.at[index, 'comments'] = ''.join([i if ord(i) < 128 else ' ' for i in row['comments']])
    #strip out all of the new line characters
    combined_df.at[index, 'comments'] = row['comments'].replace('\n', ' ')
    # build the cypher query to write the data to neo4j
    query = "MERGE (w:Well {WellName:'" + str(row.nameWell) + "'}) MERGE (e:Evidence {name: '" + str(row.comments) + "'}) MERGE (w)-[:HAS_EVIDENCE]->(e);" + "\n"
    result = session.run(query)
# Close the session
session.close()
# Close the driver
driver.close()

    
