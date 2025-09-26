import pandas as pd

def mainRead(file_path):
    df = pd.read_excel(file_path)
        
    # Remove leading and trailing spaces, line breaks, and extra spaces from column names
    df.columns = df.columns.str.strip().str.replace('\n', '').str.replace(' +', ' ', regex=True)
    # print(df.columns)

    # Get the list of current column names
    cols = df.columns.tolist()

    # Initialize counters for the two column types
    reset_amt_counter = 1
    progression_rate_counter = 1

    # Iterate over the list of column names
    for i in range(len(cols)):
        # Check if the column name matches 'Progressive Reset Amts' or 'Progressive Progression Rates'
        if cols[i] == 'Progressive Reset Amts':
            # If it matches, rename the column and increment the counter
            cols[i] = 'Progressive Reset Amts ' + str(reset_amt_counter)
            reset_amt_counter += 1
        elif cols[i] == 'Progressive Progression Rates':
            # If it matches, rename the column and increment the counter
            cols[i] = 'Progressive Progression Rates ' + str(progression_rate_counter)
            progression_rate_counter += 1
        # Check if the column name starts with 'Unnamed'
        elif 'Unnamed' in cols[i]:
            # Check if the previous column was 'Progressive Reset Amts'
            if 'Progressive Reset Amts' in cols[i-1]:
                # If it was, rename the current column and increment the counter
                cols[i] = 'Progressive Reset Amts ' + str(reset_amt_counter)
                reset_amt_counter += 1
            # Check if the previous column was 'Progressive Progression Rates'
            elif 'Progressive Progression Rates' in cols[i-1]:
                # If it was, rename the current column and increment the counter
                cols[i] = 'Progressive Progression Rates ' + str(progression_rate_counter)
                progression_rate_counter += 1

    # Assign the new column names to the DataFrame
    df.columns = cols

    # Drop rows where either 'Serial #' or 'Work Notes' is NaN
    df = df.dropna(subset=['Serial #'])
    
    # Remove rows with blank serial numbers and reset the index
    df = df[df['Serial #'] != ''].reset_index(drop=True)

    # Get all values under the Serial # column
    ws = df[['Serial #', 
            'Game Title', 
            'Game Manufacturer', 
            'Cabinet Type', 
            'Property', 
            'Zone', 
            'Bank', 
            'Loc.', 
            'Asset #', 
            'Denom (All denoms if Multi Denom)', 
            'OS Version #', 'Theo % (INC Prog)', 
            'Program Storage Media #', 
            'Paytable # (PC Chip#)', 
            'Class (II or III)', 
            'Progressive Type', 
            'Number of Progressive Levels', 
            'Progressive Reset Amts 1', 
            'Progressive Reset Amts 2', 
            'Progressive Reset Amts 3', 
            'Progressive Reset Amts 4', 
            'Progressive Reset Amts 5', 
            'Progressive Reset Amts 6', 
            'Progressive Reset Amts 7', 
            'Progressive Reset Amts 8', 
            'Progressive Progression Rates 1', 
            'Progressive Progression Rates 2', 
            'Progressive Progression Rates 3', 
            'Progressive Progression Rates 4', 
            'Progressive Progression Rates 5', 
            'Progressive Progression Rates 6', 
            'Progressive Progression Rates 7', 
            'Progressive Progression Rates 8', 
            'Top Award In Credits(If progressive enter PROG)', 
            '#Reels', 
            '#Lines', 
            'Bet per Line', 
            'Max Coin Bet (In Credits)', 
            'Bet Configuration (e.g. 1, 2, 3, 5, 10)', 
            'Boot Software/BIOS Version/Misc.',
            'Work Notes']]

    pd.set_option('display.max_columns', None)
    # print (ws)
    return ws
    
# mainRead('C:\\Users\\Paul Collins\\Dynamic Gaming Dropbox\\Dynamic Gaming Solutions (new)\\DGS Project Folder\\2024 Projects\\01 January 2024\\1.4.24 - Elk Valley - Cali - EVC 104 - DONE - SHIPPED\\EVC 104 - Project Worksheet.xlsx')