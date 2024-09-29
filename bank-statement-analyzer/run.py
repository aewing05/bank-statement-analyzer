from dbconn import update_db
from parsers import parse_file
import csv
import hashlib
import pdb
import numpy as np
import pandas as pd

from os import listdir

CSV_DIRECTORY = '/Users/aewing/Desktop/Dec-Jan Finances/'

def main():
    aggregated_data = aggregate_data(CSV_DIRECTORY)
    update_db(aggregated_data)
    return


def find_csv_filenames(path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def aggregate_data(csv_directory): 
    filenames = find_csv_filenames(csv_directory)
    dfs = []
    for file in filenames:
        full_filepath = csv_directory + file
        dfs.append(parse_file(full_filepath))

    complete_data = pd.concat(dfs, ignore_index=True)
    complete_data["category"] = np.nan
    
    complete_data["transaction_id"] = [hashlib.md5(str(x).encode('utf-8')).hexdigest() for x in complete_data.T.to_dict().values()]

    complete_data.columns = complete_data.columns.str.lower()
    complete_data = complete_data[['transaction_id', 'date', 'description', 'category', 'card_used', 'credit', 'debit']]
    
    return complete_data

if __name__ == '__main__':
    main()
