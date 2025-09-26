import os
import sys
import pymssql

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'security'))

import cipher
import keepass
import conn_module

# image_path = os.path.join(os.path.dirname(__file__), '..', 'security', 'The Man - The Myth - The Ray.jpg')

# ascii_pass = cipher.get_user_comment(image_path)

# mssql = keepass.credentials(ascii_pass)

def table_function():
    conn = conn_module.gather_conn(mssql[0], mssql[1], mssql[2], mssql[3])
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM DGS_SLOT.dbo.Master_Revenue
                Where Casino = 'Blue Lake Store'
                And date = '2024-01-31'""")
    results = cursor.fetchall()
    cursor.close()
    return results