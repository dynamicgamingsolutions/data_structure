# Import external libraries
from fuzzywuzzy import fuzz
import pandas as pd

# Define function 'master_headers'. project_headers takes in the project file in a data frame format, the normalized columns of the data frame, and the connection credentials the the MS SQL database to return standardized headers matching the required inputs for Slot Master.
def master_headers(df, new_columns, conn):
    # Store the original order of the columns
    original_order = df.columns.tolist()

    # Assign the new column names back to df.columns
    df.columns = new_columns

    # Organize columns from longest to shortest
    sorted_columns = sorted(df.columns, key=len, reverse=True)

    # Reorder the DataFrame columns
    df = df[sorted_columns]

    # SQL Connection
    cursor = conn.cursor()
    # Set query to get master headers with possible matches
    query = """SELECT * FROM analytics.dbo.fuzzy_pj_headers"""
    # Execute query
    cursor.execute(query)
    # Get results of query
    result = cursor.fetchall()

    # Initialize the list of results and the set of masters matched with numbered columns
    results = []
    numbered_masters = set()

    # Iterate over the dataframe columns
    for col in df.columns:
        # Initialize the highest score and the corresponding master
        highest_score = 0
        best_master = None
        # Iterate over the SQL results
        for row in result:
            master = row[0]
            matches = row[1:]
            # If the column does not end with a number and the master has been matched with a numbered column, skip this master
            if not col.split()[-1].isdigit() and master in numbered_masters:
                continue
            # Iterate over the matches
            for match in matches:
                # Compute the partial and complete fuzzy match scores
                partial_score = fuzz.partial_ratio(col, match)
                complete_score = fuzz.ratio(col, match)
                # Combine the scores
                score = (partial_score + complete_score) / 2
                # If the score is higher than the current highest score, update the highest score and the best master
                if score > highest_score:
                    highest_score = score
                    best_master = master
        # If the column ends with a number, add the number to the master header
        if col.split()[-1].isdigit():
            numbered_masters.add(best_master)
            best_master += '_' + col.split()[-1]
        # Add the result to the list of results
        results.append({'column': col, 'best_master': best_master, 'score': highest_score})

    # Convert the list of results into a DataFrame
    df_results = pd.DataFrame(results)

    # Create a new column for the length of the 'column' strings
    df_results['column_length'] = df_results['column'].apply(len)

    # Sort the DataFrame by score in descending order and then by column length in descending order
    df_results = df_results.sort_values(by=['score', 'column_length'], ascending=[False, False])

    # Drop the 'column_length' column
    df_results = df_results.drop(columns='column_length')

    # Drop duplicate rows based on the 'best_master' column, keeping only the first occurrence (highest score)
    df_results = df_results.drop_duplicates(subset='best_master', keep='first')

    # Create a dictionary that maps the original column names to the best matching master headers
    column_mapping = df_results.set_index('column')['best_master'].to_dict()

    # Rename the columns of df using the column_mapping dictionary
    df.columns = df.columns.map(column_mapping)

    # Create a mapping from original column names to master headers
    master_mapping = {original: column_mapping[original] for original in original_order if original in column_mapping}

    # Create a list of master headers in the original order
    master_order = [master_mapping[col] for col in original_order if col in master_mapping]

    # Reorder the DataFrame to match the original order of the master headers
    df = df[master_order]

    # Return the standardized data frame
    return df