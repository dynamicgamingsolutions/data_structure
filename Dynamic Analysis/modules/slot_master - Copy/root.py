# Import standard root libraries
import os
import sys

import pandas as pd

# Get the relative path of the subdirectory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
security_dir = os.path.join(parent_dir, 'security')
sql_dir = os.path.join(parent_dir, 'sql')
subdir_path = os.path.join(os.path.dirname(__file__), 'modules')
subMod_path = os.path.join(os.path.dirname(subdir_path), 'subModules')
head_dir = os.path.join(subMod_path, 'head_norm')

# Append subdirectory path to the system path
sys.path.append(subdir_path)
sys.path.append(security_dir)
sys.path.append(sql_dir)
sys.path.append(subMod_path)
sys.path.append(head_dir)

# Import modules from 'modules'
from modules.project_read import read_work_notes
from modules.new_project import new_project

from head_norm.head_index import project_index

#Import Sub Modules
from subModules.project_header import project_header
from subModules.project_name import project_name
from subModules.update_project import update_entry

# Import modules from 'security'
image = os.path.join(security_dir, 'The Man - The Myth - The Ray.jpg')
from cipher import get_user_comment
from keepass import credentials

# Import modules from 'sql'
from conn_module import gather_conn

# Main variables
kp_pass = get_user_comment(image)
creds = credentials(kp_pass)
conn = gather_conn(*creds)

# Modified files was located here. Temporarily replaced with functions below.

file_path = 'C:\\Users\\Paul Collins\\Dynamic Gaming Dropbox\\Dynamic Gaming Solutions (new)\\DGS Project Folder\\2024 Projects\\12 December\\12.11.24 - Rosebud Sioux - SoDak - RC 103 - DONE - SHIPPED\\RC 103 - Internal Project Worksheet.xlsx'
sheet = 'Confirmed Work Performed'

df = pd.read_excel(file_path, sheet_name=sheet, header=None)

index = project_index(df, conn)
# print(index)

df, date = project_header(file_path, sheet, conn)
# print(df)

serial_numbers, work_notes, asset_no = read_work_notes(df)
# print(serial_numbers, work_notes, asset_no)

project = project_name(file_path)
# print(project)

cursor = conn.cursor()
query = """SELECT project_name FROM analytics.dbo.project_list"""
cursor.execute(query)

# Fetch all rows from the last executed statement
results = cursor.fetchall()

# Check if project is in results
project_in_results = False
for row in results:
    if project == row[0]:  # Compare project with the first column of the row
        project_in_results = True
        break

# print('Project in results:', project_in_results)

if project_in_results == True:
    update_entry(df, conn)
else:
    new_project(df, date, conn, creds, project)
