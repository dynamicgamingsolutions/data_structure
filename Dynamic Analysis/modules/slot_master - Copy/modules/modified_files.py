import os
import fnmatch
from datetime import datetime
import re

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern) and not basename.startswith('~$'):
                filename = os.path.join(root, basename)
                yield filename
                
def modified_files(directory, pattern):
    for filename in find_files(directory, pattern):
        # Get the last modification time and the current time
        mod_time = os.path.getmtime(filename)
        mod_time = datetime.fromtimestamp(mod_time)
        current_time = datetime.now()

        # Check if the file was modified since the 1st of the current month
        if mod_time.year == current_time.year and mod_time.month == current_time.month and mod_time.day >= 1:
            # Extract the date from the file path
            match = re.search(r'\d{1,2}\.\d{1,2}\.\d{2}', filename)
            if match:
                date_str = match.group(0)
                date = datetime.strptime(date_str, "%m.%d.%y")
                date_str = date.strftime("%Y-%m-%d")
            else:
                date_str = "TBD"

            print('Found:', filename, ', Last modified on:', mod_time.strftime("%Y-%m-%d %H:%M:%S"), ', Date in path:', date_str)
            
# modified_files('C:\\Users\\Paul Collins\\Dynamic Gaming Dropbox\\Dynamic Gaming Solutions (new)\\DGS Project Folder', '*- Project Worksheet.xlsx')