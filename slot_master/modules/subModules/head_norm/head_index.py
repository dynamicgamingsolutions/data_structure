# Import external libraries
from fuzzywuzzy import fuzz
import numpy as np
import scipy
from scipy.signal import find_peaks


# import pymssql
# import pandas as pd

# conn = pymssql.connect(
#     server='192.168.1.195',
#     user='paulc',
#     password='092@290Mxx',
#     database='analytics')

# file_path = 'C:\\Users\\Paul Collins\\Dynamic Gaming Dropbox\\Dynamic Gaming Solutions (new)\\DGS Project Folder\\2025 Projects\\04 April\\4.16.25 - Chicken Ranch - Cali - CRC 108\\CRC 108 - Internal Project Worksheet SM.xlsx'
# sheet = 'Confirmed Work Performed'

# df = pd.read_excel(file_path, sheet_name=sheet, header=None)

# Define function 'project_index'. project_index takes in the file path for a project file and the connection credentials for the MS SQL database to return the most likely starting index for the headers in the project file.
def project_index(file_path, conn):
    cursor = conn.cursor()
    query = """SELECT * FROM analytics.dbo.fuzzy_pj_headers"""
    cursor.execute(query)
    result = cursor.fetchall()

    avg_scores = []  # List to store average scores
    for i, row in file_path.iterrows():
        total_score = 0
        for value in row.values:
            if str(value).lower() == 'nan':
                highest_score = 0
            else:
                highest_score = max(fuzz.partial_ratio(str(value), match) for row in result for match in row[1:] if match != 'NULL')
            total_score += highest_score
        avg_score = total_score / len(row.values)
        avg_scores.append(avg_score)  # Add average score to the list

    threshold = 2 * np.mean(avg_scores)  # Set threshold as an index percentage of the average score
    peaks, _ = scipy.signal.find_peaks(avg_scores, height=threshold)  # Find peaks in the average scores above the threshold

    return peaks  # Return the peaks directly

# peaks = project_index(df, conn)
# print(peaks)