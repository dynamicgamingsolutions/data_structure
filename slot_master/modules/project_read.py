def read_work_notes(df):    
    # Get all values under the Work Notes column
    work_notes = df['notes']
    
    # Get all values under the Serial # column
    serial_numbers = df['serial_no']
    
    #Get all values under the Asset # column
    asset_numbers = df['asset_no']

    return serial_numbers, work_notes, asset_numbers