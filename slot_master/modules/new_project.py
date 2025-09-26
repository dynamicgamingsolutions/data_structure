import os
import sys
import datetime

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
subModule_dir = os.path.join(current_dir, 'subModules')

sys.path.append(subModule_dir)

from deactivate import deactivate_query
from insert import insert_setup
from install_format import install_format

def new_project(df, date, conn, creds, project):
    
    pj_cursor = conn.cursor()
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    pj_cursor.execute(f"""INSERT INTO analytics.dbo.project_list (project_name, project_date, last_modified) VALUES ('{project}', '{date}', '{current_date}')""")
    
    deactivate = ['REMOVAL', 'CONVERT FROM', 'BANK MOVE FROM', 'RECONFIGURE FROM']
    # Iterate over the rows of the dataframe
    for index, row in df.iterrows():
        # If the 'notes' column of the row contains any of the values in 'deactivate'
        if any(item in row['notes'] for item in deactivate):
            # Pass the row, date, and conn to the 'deactivate_query' function
            deactivate_query(row, date, conn)
    # Assuming 'activate' is the list of cabinet info that needs to be added
    activate = ['INSTALL', 'CONVERT TO', 'BANK MOVE TO', 'RECONFIGURE TO']
    
    # Create an empty DataFrame to store the processed rows
    result_df = pd.DataFrame()
    
    for index, row in df.iterrows():
        # If the 'notes' column of the row contains any of the values in 'activate'
        if any(item in row['notes'] for item in activate):
            # Process the row that needs to be added
            entry = insert_setup(row, date, conn, creds, project)

            # Format the entry for insertion
            entry = install_format(entry, date)

            placeholders = ', '.join(['%s'] * len(entry))
            cursor = conn.cursor()
            cursor.execute(f"EXEC analytics.dbo.InsertIntoSlotMaster {placeholders}", tuple(entry.tolist()))
            conn.commit()
            
            # Convert the Series to a DataFrame and transpose it
            entry_df = pd.DataFrame(entry).transpose()

            # Append the processed row to the result DataFrame
            result_df = pd.concat([result_df, entry_df], ignore_index=True)

    # Return the result DataFrame
    return result_df
                
            
# Set display options and return df
pd.set_option('display.max_columns', None)

# print(new_project(df, date, conn, creds, project))