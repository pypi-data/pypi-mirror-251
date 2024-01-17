import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# # Install required packages
# install('pandas')
# install('openpyxl')
# install('numpy')
# install('anonymizedf')

import pandas as pd
import numpy as np
from anonymizedf.anonymizedf import anonymize

def add_noise(df, column, std=None):
    if df[column].dtype.kind in 'biufc':  # Check if the column is numeric
        if std is None:
            std = df[column].std()
        with_noise = df[column].add(np.random.normal(0, std, df.shape[0]))
        return with_noise
    else:
        return df[column]  # Return original column if it's not numeric

def simple_obfuscate(cell):
    if pd.isnull(cell):  # Keep null values
        return cell
    if isinstance(cell, (int, float)):  # Add random number to numeric values
        return cell + np.random.randint(-100, 100)
    if isinstance(cell, str):  # Shift characters in string values
        return ''.join(chr((ord(c) - 96 + 10) % 26 + 96) if c.isalpha() else c for c in cell)
    return cell  # Return original value if not null, numeric, or string

def obfuscate_columns(file_name, method, column_range):
    base_file_name = os.path.splitext(os.path.basename(file_name))[0]
    df = pd.read_excel(file_name)
    
    print()
    print('before :')
    print('-------')
    print(df)

    # Split column range and convert to integers
    range_parts = column_range.split(':')
    if range_parts[0] == '':
        start_index = 0
    else:
        start_index = int(range_parts[0])
    
    if range_parts[1] == '':
        end_index = len(df.columns) - 1
    else:
        end_index = int(range_parts[1])

    columns = df.columns[start_index:end_index+1]  # Get columns within range (end index is inclusive)
    
    if method == 'simple':
        for column in columns:
            df[column] = df[column].apply(simple_obfuscate)
    elif method == 'anonymizedf':
        an = anonymize(df)
        for column in columns:
            an.fake_whole_numbers(column)
    elif method == 'perturb':
        for column in columns:
            df[column] = add_noise(df, column)
    
    df.to_excel(f"obfuscated_{base_file_name}_{method}.xlsx", index=False)
    print()
    print('after :')
    print('-------')
    print(df)

if __name__ == "__main__":
    file_path = sys.argv[1]
    method = sys.argv[2]
    column_range = sys.argv[3]
    obfuscate_columns(file_path, method, column_range)