def deactivate_query(row, date, conn):
    set_statements = []
    where_statements = []

    note = row.get('notes', '')

    if 'REMOVE' in note:
        set_statements.append(f"rmvl_date = '{date}'")

    serial_no = row['serial_no']
    if isinstance(serial_no, (int, float)):
        serial_no = int(serial_no)
    where_statements.append(f"serial_no = '{serial_no}'")  # Add this line

    set_clause = ', '.join(set_statements)
    where_clause = ' AND '.join(where_statements)

    if set_clause:
        set_clause = ', ' + set_clause

    query = f"""UPDATE analytics.dbo.slot_master
                SET 
                    active = 'Inactive'{set_clause}
                WHERE
                    {where_clause}
                AND
                    active = 'Active'
                """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    # return query