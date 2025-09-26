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

def modified_files(directory, pattern, year, month):
    printed_files = set()
    for filename in find_files(directory, pattern):
        # Extract the date from the file path
        match = re.search(r'\d{1,2}\.\d{1,2}\.\d{2}', filename)
        if match:
            date_str = match.group(0)
            date = datetime.strptime(date_str, "%m.%d.%y")  # Changed from %Y to %y
            date_str = date.strftime("%Y-%m-%d")

            # Check if the date is in January 2024
            if date.year == year and date.month == month:
                basename = os.path.basename(filename)
                if basename not in printed_files:
                    #print('Found:', filename, ', Date in path:', date_str)
                    #printed_files.add(basename)
                    return filename, date_str

# modified_files('C:\\Users\\Paul Collins\\Dynamic Gaming Dropbox\\Dynamic Gaming Solutions (new)\\DGS Project Folder', '*- Project Worksheet.xlsx')