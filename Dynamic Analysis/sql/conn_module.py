import os
import pymssql

def gather_conn(server_ip, user, password, database):
    # Open the connection
    conn = pymssql.connect(
        server=server_ip,
        user=user,
        password=password,
        database=database)
    return conn