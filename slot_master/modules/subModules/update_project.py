import math
import pymssql


def try_float(value):
    if value is None:
        return None
    try:
        # Check if the value is a string
        if isinstance(value, str):
            # Strip all but the first line
            value = value.split('\n')[0]
            # Check if the value ends with a '%'
            if '%' in value:
                # If it does, remove the '%' and convert to a float
                float_value = float(value.strip('%')) / 100
                # Format the float value
                return "{:.2f}".format(float_value)
        # If the value is not a string or doesn't end with a '%', return None
        return None
    except ValueError:
        # If the conversion fails, return None
        return None

def try_int(value):
    if value is None:
        return None
    try:
        # Check if the value is a string
        if isinstance(value, str):
            # Strip all but the first line
            value = value.split('\n')[0]
            # Check if the value is blank
            if value == '':
                return None
        float_value = float(value)
        if math.isnan(float_value):  # Check if the value is NaN
            return None  # or return some default value
        else:
            return str(int(float_value))
    except ValueError:
        return str(value)

def entry(index, df):
    theo_hold = try_float(df['theo_hold'].values[index])
    df_entry = (try_int(df['zone'].values[index]),
                try_int(df['bank'].values[index]),
                try_int(df['location'].values[index]),
                try_int(df['asset_no'].values[index]),
                df['serial_no'].values[index],
                df['theme'].values[index],
                df['manufac'].values[index],
                df['model_no'].values[index],
                str(df['denom'].values[index]).replace('\n', '/').replace('$',''),
                df['boot_bios'].values[index],
                df['os_version'].values[index],
                df['prog_media'].values[index],
                str(df['paytable'].values[index]).split('\n')[0],
                theo_hold,
                try_float(1 - float(theo_hold) if theo_hold is not None else None),
                try_int(df['top_award'].values[index]),
                try_int(df['reels'].values[index]),
                try_int(df['no_lines'].values[index]),
                str(df['bet_line'].values[index]).split('\n')[0],
                try_int(df['maxcoinbet'].values[index]),
                df['betconfig'].values[index],
                df['prog_type'].values[index],
                try_int(df['prog_level'].values[index]),
                try_int(df['reset_1'].values[index]),
                try_int(df['reset_2'].values[index]),
                try_int(df['reset_3'].values[index]),
                try_int(df['reset_4'].values[index]),
                try_int(df['reset_5'].values[index]),
                try_int(df['reset_6'].values[index]),
                try_int(df['reset_7'].values[index]),
                try_int(df['reset_8'].values[index]),
                try_float(df['prog_1'].values[index]),
                try_float(df['prog_2'].values[index]),
                try_float(df['prog_3'].values[index]),
                try_float(df['prog_4'].values[index]),
                try_float(df['prog_5'].values[index]),
                try_float(df['prog_6'].values[index]),
                try_float(df['prog_7'].values[index]),
                try_float(df['prog_8'].values[index]))
    return df_entry

def update_entry(df, conn):
    cursor = conn.cursor()
    
    notes_to_search = ['CONVERT TO', 'INSTALL', 'BANK MOVE TO', 'RECONFIGURE TO']
    entries = []
    # Iterate over the DataFrame rows where 'notes' is in notes_to_search
    for index, row in df[df['notes'].isin(notes_to_search)].iterrows():
        entry_values = entry(index, df)
        placeholders = ', '.join(['%s'] * len(entry_values))
        query = f"EXEC analytics.dbo.UpdateSlotMaster {placeholders}"
        try:
            cursor.execute(query, entry_values)
        except pymssql.ProgrammingError as e:
            print(f"Error executing query: {e}")
            continue
        entries.append(entry_values)
        
    conn.commit()  # Commit the transaction
    return entries