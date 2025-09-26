import os
import sys
import pykeepass

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the relative paths
kp_path = os.path.join(script_dir, 'pass_database.kdbx')
keyfile_path = os.path.join(script_dir, 'keyfile', 'pass_key_file.keyx')

# kp_password = """±:6ã¹Öà/¥_`©8«wáÁfaÞNPÑùçSðüá*Zð¬èâ´ÁËP"x¿©ÜÎn2ÃXÿä<(§÷~MæTÂ+·'wÝ°@±.'ädæ¥Ü*?åPÎ¤QâÃÉéÛzpÜ½ãû×íËdÚ¡¦oRe2E*n^ò5u@Ë¿þùõ÷+jZáÄ¿r\ø7"""

def credentials(kp_password):
    kp = pykeepass.PyKeePass(kp_path, password=kp_password, keyfile=keyfile_path)
    entry = kp.find_entries(title='DGS MSSQL Server', first=True)
    server_ip = entry.get_custom_property('Server IP')
    user = entry.username
    password = entry.password
    database = entry.get_custom_property('Database')
    return server_ip, user, password, database