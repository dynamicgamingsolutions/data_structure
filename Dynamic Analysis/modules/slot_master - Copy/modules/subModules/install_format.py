import math
import datetime
from datetime import datetime
import pandas as pd

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
    
def parse_date(date):
    for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def try_date(value):
    if value is None:
        return None
    try:
        if isinstance(value, pd.Timestamp):
            return value.strftime('%Y-%m-%d')
        else:
            return parse_date(value).strftime('%Y-%m-%d')
    except ValueError:
        return None

def install_format(row, date):       
    row['compid'] = row['serial_no'] #compid [0]
    row['zone'] = try_int(row['zone']) #zone [10]
    row['bank'] = try_int(row['bank']) #bank [11]
    row['location'] = try_int(row['location']) #location [12]
    row['asset_no'] = try_int(row['asset_no']) #asset_no [13]
    row['denom'] = str(row['denom']).replace('\n', '/').replace('$','') #denom [14]
    row['theo_hold'] = try_float(row['theo_hold'])
    if row['theo_hold'] is not None:
        row['Hold'] = "{:.2%}".format(1 - float(row['theo_hold']))
    else:
        row['Hold'] = None
    row['paytable'] = str(row['paytable']).split('\n')[0] #paytable [21]
    row['date_instl'] = try_date(row['date_instl']) #date_instl [22]
    row['golive001'] = try_date(row['golive001']) #golive001 [23]
    row['lastconver'] = try_date(row['lastconver']) #lastconver [24]
    row['rmvl_date'] = try_date(row['rmvl_date']) #rmvl_date [25]
    row['prog_level'] = try_int(row['prog_level']) #prog_level [28]
    row['reset_1'] = try_float(row['reset_1']) #reset_1 [29]
    row['reset_2'] = try_float(row['reset_2']) #reset_2 [30]
    row['reset_3'] = try_float(row['reset_3']) #reset_3 [31]
    row['reset_4'] = try_float(row['reset_4']) #reset_4 [32]
    row['reset_5'] = try_float(row['reset_5']) #reset_5 [33]
    row['reset_6'] = try_float(row['reset_6']) #reset_6 [34]
    row['reset_7'] = try_float(row['reset_7']) #reset_7 [35]
    row['reset_8'] = try_float(row['reset_8']) #reset_8 [36]
    row['prog_1'] = try_float(row['prog_1']) #prog_1 [37]
    row['prog_2'] = try_float(row['prog_2']) #prog_2 [38]
    row['prog_3'] = try_float(row['prog_3']) #prog_3 [39]
    row['prog_4'] = try_float(row['prog_4']) #prog_4 [40]
    row['prog_5'] = try_float(row['prog_5']) #prog_5 [41]
    row['prog_6'] = try_float(row['prog_6']) #prog_6 [42]
    row['prog_7'] = try_float(row['prog_7']) #prog_7 [43]
    row['prog_8'] = try_float(row['prog_8']) #prog_8 [44]
    row['top_award'] = try_int(row['top_award']) #top_award [45]
    row['reels'] = try_int(row['reels']) #reels [46]
    row['no_lines'] = try_int(row['no_lines']) #no_lines [47]
    row['bet_line'] = str(row['bet_line']).split('\n')[0] #bet_line [48]
    row['maxcoinbet'] = try_int(row['maxcoinbet']) #maxcoinbet [49]
    row['ref_day001'] = try_date(row['ref_day001']) #ref_day001 [62]
    row['agrordate'] = try_date(row['agrordate']) #agrordate [64]
    row['purch_date'] = try_date(row['purch_date']) #purch_date [66]
    row['active'] = 'Active' #active [68]

    return row