# Import native libraries
import os
import sys
import re
from datetime import datetime

# Import external libraries
import pandas as pd

# "head_norm" path append
current_dir = os.path.dirname(os.path.abspath(__file__))
subMod_dir = os.path.join(current_dir, 'head_norm')
sys.path.append(subMod_dir)

# 'head_norm' modules
from head_index import project_index
from normalize_dataframe import normalize_dataframe
from master_match import master_headers
from conform import conform_dataframe

def project_header(file_name, sheet, conn):
    # Set Excel file to dataframe
    df = pd.read_excel(file_name, sheet_name=sheet, header=None)

    # Find header(s) index
    header_row_index = project_index(df, conn)

    if len(header_row_index) > 1:
        # If header_row_index contains more than one value, call conform_dataframe
        df = conform_dataframe(conn, file_name, sheet, header_row_index)
    else: 
        #Assign index to header_row_index if it is not empty
        df = pd.read_excel(file_name, sheet_name=sheet, header=5)

    # Normalize the dataframe
    df, new_columns = normalize_dataframe(df)
    #Match the headers to the master headers
    df = master_headers(df, new_columns, conn)
    # Drop rows where either 'Serial #' is NaN
    df = df.dropna(subset=['serial_no'])
    # Reset the index
    df = df.reset_index(drop=True)
    
    
    
    match = re.search(r'\d{1,2}\.\d{1,2}\.\d{2}', file_name)
    date_str = match.group(0)
    date = datetime.strptime(date_str, "%m.%d.%y")
    date_str = date.strftime("%Y-%m-%d")
    
    return df, date_str