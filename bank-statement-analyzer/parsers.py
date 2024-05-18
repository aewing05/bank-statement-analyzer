import numpy as np
import pandas as pd

def parse_file(file):
    if 'amex' in file:
        return amex_csv_parser(file)
    elif 'capitalone' in file:
        return capitalone_csv_parser(file)
    elif 'chase' in file:
        return chase_csv_parser(file)
    elif 'discover' in file:
        return discover_csv_parser(file)
    elif 'schwab' in file:
        return schwab_csv_parser(file)
    elif 'nordstrom' in file:
        return nordstrom_csv_parser(file)
    else:
        raise Exception("The CSV file could not be identified: ", file)

def amex_csv_parser(file):
    df = pd.read_csv(file).drop(columns=['Card Member', 'Account #'])
    df['Debit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x < 0 else np.NaN)
    df['Credit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x > 0 else np.NaN)
    df['Card Used'] = get_card_used(file, 'amex')
    return df.drop(columns=['Amount'])

def capitalone_csv_parser(file):
    df = pd.read_csv(file).drop(columns=['Posted Date', 'Card No.', 'Category']).rename(columns={"Transaction Date": "Date"})
    df['Card Used'] = get_card_used(file, 'capitalone')
    return df

def chase_csv_parser(file):
    df = pd.read_csv(file).drop(columns=['Post Date', 'Category', 'Type', 'Memo']).rename(columns={"Transaction Date": "Date"})
    df['Debit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x < 0 else np.NaN)
    df['Credit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x > 0 else np.NaN)
    df['Card Used'] = get_card_used(file, 'chase')
    return df.drop(columns=['Amount'])

def discover_csv_parser(file):    
    df = pd.read_csv(file).drop(columns=['Post Date', 'Category']).rename(columns={"Trans. Date": "Date"})
    df['Debit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x < 0 else np.NaN)
    df['Credit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x > 0 else np.NaN)
    df['Card Used'] = get_card_used(file, 'discover')
    return df.drop(columns=['Amount'])

def nordstrom_csv_parser(file):
    df = pd.read_csv(file).rename(columns=lambda x: x.strip()).drop(columns=['Posting Date', 'Ref#']).rename(columns={"Transaction Date": "Date", "Transaction Detail": "Description"})
    df['Card Used'] = get_card_used(file, 'nordstrom')
    df['Debit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x < 0 else np.NaN)
    df['Credit'] = df['Amount'].astype(float).apply(lambda x: abs(x) if x > 0 else np.NaN)
    df = df.drop(columns=['Amount'])
    return df

def schwab_csv_parser(file):
    df = pd.read_csv(file).drop(columns=['Status', 'Type', 'CheckNumber', 'RunningBalance']).rename(columns={"Withdrawal": "Credit", "Deposit": "Debit"})
    df['Card Used'] = get_card_used(file, 'schwab')
    return df

def get_card_used(file, bank):
    file = file.removesuffix('.csv')
    return file[file.find(bank):]

