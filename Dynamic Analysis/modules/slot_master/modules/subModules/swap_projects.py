# Import external libraries (check requirements.txt and if updates needed)
import pymssql
import pandas as pd

# Gather data from project worksheet for conversion projects (Called from conversion_insert)
def conversion_read(file_path, state, convert_date, project):

    # Build dataframe from project worksheet
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.replace('\n', '')
    df = df.dropna(subset=['Serial #'])
    df = df[df['Serial #'] != ''].reset_index(drop=True)

    # Define variables not in Project Worksheet (Either from project file name or SQL table)
    state = state
    convert_date = convert_date
    project = project

    # Create two new dataframes: one for 'REMOVE' and one for 'INSTALL'
    df_from = df[df['Work Notes'] == 'REMOVE']
    df_to = df[df['Work Notes'] == 'INSTALL']

    # Rename the 'Game Title' column in both dataframes to avoid a naming conflict when merging
    df_from = df_from.rename(columns={'Game Title': 'Theme From'})
    df_to = df_to.rename(columns={'Game Title': 'Theme To'})

    # Merge the two dataframes on the 'Serial #' column
    df_merged = pd.merge(df_from, df_to, on='Serial #', suffixes=('_from', '_to'))

    # Create an empty list to store the rows
    rows = []
    
    # Now you can append each row to the list
    for row in df_merged.iterrows():
        rows.append((row['Property_from'], state, row['Game Manufacturer_from'], row['Cabinet Type_from'], row['Serial #'], row['Theme From'], row['Theme To'], convert_date, project))

    # Return the list of rows
    return rows

# Insert data into the database (Called from root.py)
def conversion_insert(file_path, state, convert_date, project, creds):
    
    #Establish connection to the SQL server
    conn = pymssql.connect(
    server=creds[0],
    user=creds[1],
    password=creds[2],
    database=creds[3]
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Call the conversion_read function to get information from the Project Worksheet
    rows = conversion_read(file_path, state, convert_date, project)
    
    # Prepare the SQL query
    sql = """EXEC analytics.dbo.conversion_log 
                @casino = %s, 
                @state = %s, 
                @manufacturer = %s, 
                @cabinet = %s, 
                @serial_number = %s,  
                @convert_from = %s, 
                @convert_to = %s, 
                @convert_date = %s, 
                @project = %s"""

    # Execute the SQL query for each row
    for row in rows:
        cursor.execute(sql, row)

    # Commit the changes and close the cursor
    conn.commit()
    cursor.close()

    # Return the rows
    return rows