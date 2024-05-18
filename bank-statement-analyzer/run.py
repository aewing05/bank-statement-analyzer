from parsers import parse_file

import csv
import numpy as np
import pandas as pd

import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from os import listdir
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

CSV_DIRECTORY = '/Users/aewing/Desktop/Dec-Jan Finances/'
SHEET_KEY = '1HkcYF_-pmO9ZCDPQuGNzt7HOf_jfcL1FcfUifNN1FOs'
WORKSHEET_NAME = 'raw_data'

def main():
    aggregated_data = aggregate_data(CSV_DIRECTORY)
    append_data_to_gsheet(aggregated_data, SHEET_KEY, WORKSHEET_NAME)
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
    complete_data["Category"] = np.nan
    complete_data = complete_data[['Date', 'Description', 'Category', 'Card Used', 'Credit', 'Debit']]
    return complete_data

def append_data_to_gsheet(data, sheet_key, worksheet_name):
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

    credentials = Credentials.from_service_account_file('../credentials.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    
    # open a google sheet
    gs = gc.open_by_key(sheet_key)
    # select a work sheet from its name
    ws = gs.worksheet(worksheet_name)

    data_list = data.fillna('').values.tolist()
    if ws.acell('A1').value == None:
        headers = data.columns.tolist()
        data_list.insert(0, headers)

    gs.values_append(worksheet_name, {'valueInputOption': 'RAW'}, {'values': data_list})

if __name__ == '__main__':
    main()
