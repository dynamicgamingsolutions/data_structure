# Define 'normalize_dataframe'. normalize_dataframe removes leading/trailing spaces, removes line breaks, removes extra spaces, and converts headers to lower case. After normalizing, a header is applied to any columns listed as unnamed using the most recent header name, and adding a sequential number pattern to the end.
def normalize_dataframe(df):
    # Convert column names to strings
    df.columns = df.columns.astype(str)

    # Normalize columns
    df.columns = df.columns.str.strip().str.replace('\n', '').str.replace(' +', ' ', regex=True).str.lower()

    # Create a new list of column names
    new_columns = []

    # Keep track of the last non-'unnamed' header
    last_header = None

    # Iterate over the headers
    for i, header in enumerate(df.columns):
        if 'unnamed' not in header:
            # If the header is not 'unnamed', update last_header
            last_header = header
            # If the next header is 'unnamed', add '1' to the current header
            if i < len(df.columns) - 1 and 'unnamed' in df.columns[i + 1]:
                last_header += ' 1'
            new_columns.append(last_header)
        else:
            # If the header is 'unnamed', use last_header as the base and increment the counter
            if ' ' in last_header:
                number = int(last_header.split(' ')[-1]) + 1
                last_header = ' '.join(last_header.split(' ')[:-1]) + ' ' + str(number)
            else:
                last_header += ' 1'
            new_columns.append(last_header)
            
    df.columns = new_columns
    # Return data frame and data frame headers.
    return df, new_columns