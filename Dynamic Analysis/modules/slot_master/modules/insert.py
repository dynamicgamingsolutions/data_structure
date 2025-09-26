import os
import sys
from fuzzywuzzy import fuzz, process
import pandas as pd
import pymssql

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
security_dir = os.path.join(parent_dir, 'security')
sql_dir = os.path.join(parent_dir, 'sql')

sys.path.append(security_dir)
sys.path.append(sql_dir)

image = os.path.join(security_dir, 'The Man - The Myth - The Ray.jpg')
from cipher import get_user_comment
from keepass import credentials
from conn_module import gather_conn

# Main variables
kp_pass = get_user_comment(image)
creds = credentials(kp_pass)
conn = gather_conn(*creds)


def old_conn(server, user, password, database):
    return pymssql.connect(server=server, user=user, password=password, database=database)

# Define a function to apply the conditional logic
def apply_date(row, date):
    if row['notes'] == 'CONVERT TO':
        row['lastconver'] = date
    elif row['notes'] == 'INSTALL':
        row['date_instl'] = date
    return row

def match_name(name, name_list, min_score=0):
    match = process.extractOne(name, name_list, scorer=fuzz.token_sort_ratio, score_cutoff=min_score)
    return match[0] if match else None

def reorder_row(row, proc_name, conn, vendor_df, cabinet_df, theme_df):
    cursor = conn.cursor()
    cursor.callproc('sp_procedure_params_rowset', (proc_name, None, None, None))
    params = [row[3].replace('@', '') for row in cursor]
    cursor.close()

    new_row = row.copy()
    for param in params:
        if param not in new_row.index:
            new_row[param] = None

    new_row = new_row.reindex(params)
    new_row['manufac'] = match_name(new_row['manufac'], vendor_df['vendor'])
    new_row['model_no'] = match_name(new_row['model_no'], cabinet_df['cabinet'])
    new_row['theme'] = match_name(new_row['theme'], theme_df['theme'])

    return new_row

def insert_setup(row, date, conn, creds, project):
    # Convert the 'date' string to a datetime object
    date = pd.to_datetime(date)

    # Establish DGS connection
    dgs_conn = old_conn(creds[0], creds[1], creds[2], 'DGS_SLOT')
    dgs_cursor = dgs_conn.cursor()

    # Execute queries
    query_vendor = "SELECT * FROM DGS_SLOT.dbo.vendor"
    query_cabinet = "SELECT * FROM DGS_SLOT.dbo.cabinet"
    theme_query = "SELECT * FROM DGS_SLOT.dbo.theme"
    dgs_cursor.execute(query_vendor)
    vendor = dgs_cursor.fetchall()
    dgs_cursor.execute(query_cabinet)
    cabinet = dgs_cursor.fetchall()
    dgs_cursor.execute(theme_query)
    theme = dgs_cursor.fetchall()

    # Create dataframes
    vendor_df = pd.DataFrame(vendor, columns=['ID', 'vendor'])
    cabinet_df = pd.DataFrame(cabinet, columns=['ID', 'cabinet'])
    theme_df = pd.DataFrame(theme, columns=['ID', 'theme'])

    # Apply date
    row = apply_date(row, date)

    # Reorder row
    row = reorder_row(row, 'InsertIntoSlotMaster', conn, vendor_df, cabinet_df, theme_df)

    # Get project and abrev
    abrev = project.split(' ')[0]
    row['abrev'] = abrev

    # Execute casino query
    cursor = conn.cursor()
    casino_query = "SELECT * FROM analytics.dbo.casino_names"
    cursor.execute(casino_query)
    casino = cursor.fetchall()

    # Create casino dataframe
    casino_df = pd.DataFrame(casino, columns=['sql_casino','official_casino','casino_id','casino_abrv','back_os','sql_tribe','official_tribe','state','address_full','address','city','state_abbreviation','zip','Longitude','Latitude', 'sales', 'UniqueID'])

    # Match property and abrev
    row['property'] = match_name(str(row['property']), casino_df['official_casino'])
    row['abrev'] = match_name(str(row['abrev']), casino_df['casino_abrv'])
    
    # Drop 'RETURN_VALUE' and 'abrev' columns
    row = row.drop(labels=['RETURN_VALUE', 'abrev'])

    # Create dictionaries
    casino_dict = dict(zip(casino_df['official_casino'], zip(casino_df['state'], casino_df['official_tribe'], casino_df['back_os'])))

    # Map the dictionary to df
    row['state'], row['tribe'], row['back_os'] = casino_dict.get(row['property'], (None, None, None))

    return row