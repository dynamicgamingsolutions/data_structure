import pandas as pd
from fuzzywuzzy import fuzz

def conform_dataframe(conn, file_name, sheet, header_index_row):
    cursor = conn.cursor()
    query = """SELECT * FROM analytics.dbo.fuzzy_pj_headers"""
    cursor.execute(query)
    result = cursor.fetchall()

    # Set the display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Calculate the number of rows to read
    nrows = header_index_row[1] - header_index_row[0] - 1

    # Read the specified range of rows from the Excel file, treating the first row as headers
    df = pd.read_excel(file_name, sheet_name=sheet, header=header_index_row[0], nrows=nrows)

    # Convert all headers to strings, then strip extra spaces and convert to lower case
    headers = df.columns.astype(str).str.strip().str.lower().tolist()

    # Initialize an empty set to store seen headers
    seen = set()

    # Initialize repeated_header and split_index to None
    repeated_header = None
    split_index = None

    # Iterate over the headers
    for i, header in enumerate(headers):
        # Ignore the .1 suffix
        header_no_suffix = header.rsplit('.', 1)[0]
        if header_no_suffix in seen:
            # If the header (without the suffix) has been seen before, it's a repeated header
            repeated_header = header_no_suffix
            split_index = i
            break
        else:
            # Otherwise, add it to the set of seen headers
            seen.add(header_no_suffix)

    if repeated_header is not None:
        # If a repeated header was found, split the DataFrame
        df_old = df.iloc[:, :split_index]
        df_new = df.iloc[:, split_index:]
    else:
        print("No repeated headers found.")
        # Initialize df_old and df_new to avoid UnboundLocalError
        df_old = df.iloc[:, :]
        df_new = pd.DataFrame()  # Empty DataFrame for df_new

    # Identify the Progressive Set
    # This is a placeholder, replace it with your actual code
    df_prog = pd.read_excel(file_name, sheet_name=sheet, header=header_index_row[1])

    # Initialize dictionaries to store the best match and its score for each header
    best_matches_new = {}
    best_matches_prog = {}

    # Iterate over the tuples in result
    for result_tuple in result:
        # Convert the master header and match options to strings
        master_header = str(result_tuple[0]).lower()
        headers_to_match = [str(header).lower() for header in result_tuple[1:]]

        # If the master header is 'theme', proceed
        if master_header == 'theme':
            # Iterate over the headers in df_new
            for header in df_new.columns:
                # Convert header to lowercase
                header_lower = header.lower()
                # Find the best fuzzy match in df_new.columns for each header_to_match using partial_ratio
                for header_to_match in headers_to_match:
                    match_score = fuzz.partial_ratio(header_lower, header_to_match)
                    # If this score is the best so far for this header, store it in the dictionary
                    if header not in best_matches_new or match_score > best_matches_new[header][1]:
                        best_matches_new[header] = (header_to_match, match_score)

            # Iterate over the headers in df_prog
            for header in df_prog.columns:
                # Convert header to lowercase
                header_lower = header.lower()
                # Find the best fuzzy match in df_prog.columns for each header_to_match using partial_ratio
                for header_to_match in headers_to_match:
                    match_score = fuzz.partial_ratio(header_lower, header_to_match)
                    # If this score is the best so far for this header, store it in the dictionary
                    if header not in best_matches_prog or match_score > best_matches_prog[header][1]:
                        best_matches_prog[header] = (header_to_match, match_score)

    # Find the header with the highest score in df_new and df_prog
    new_theme_name = max(best_matches_new, key=lambda header: best_matches_new[header][1])
    prog_theme_name = max(best_matches_prog, key=lambda header: best_matches_prog[header][1])

    # Get the column index of the best match in df_new and df_prog
    new_theme_index = df_new.columns.get_loc(new_theme_name)
    prog_theme_index = df_prog.columns.get_loc(prog_theme_name)

    # Create a mapping from df_prog values to themselves
    mapping = pd.Series(df_prog.iloc[:, prog_theme_index].values, index=df_prog.iloc[:, prog_theme_index]).to_dict()

    # Create a new column in df_new with the matched values from df_prog
    df_new['Matched'] = df_new.iloc[:, new_theme_index].map(mapping).fillna('N/A')

    # Merge df_new and df_prog on the 'Matched' column and the column of interest in df_prog
    df_new = df_new.merge(df_prog, left_on='Matched', right_on=df_prog.columns[prog_theme_index], how='left')

    # Delete the 'Matched' column and the column associated with 'prog_theme_name'
    df_new = df_new.drop(columns=['Matched', prog_theme_name])

    # # Remove the first column of df_old
    df_old = df_old.iloc[:, 1:]

    # Match the headers in df_old and df_new using fuzzy matching
    matched_headers = {}
    for old in df_old.columns:
        # Find the best match in df_new.columns that is not already in matched_headers.values()
        best_match = max((new for new in df_new.columns if new not in matched_headers.values()),
                        key=lambda new: fuzz.partial_ratio(old, new), default=None)
        if best_match is not None:
            matched_headers[old] = best_match

    # Rename the headers in df_old to match those in df_new
    df_old = df_old.rename(columns=matched_headers)

    # Vertically stack df_old and df_new
    df_combined = pd.concat([df_old, df_new], ignore_index=True)

    return df_combined,df_old