import os
import re

def project_name(file_path):
    # Get the file name from the file path
    file_name = os.path.basename(file_path)

    # Split the file name at ' - ' and get the first part
    project_name = re.split(' - ', file_name)[0]

    return project_name