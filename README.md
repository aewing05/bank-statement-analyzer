# bank-statement-analyzer

## Setup
1. Clone Repo
2. In repo directory, create a virtual environment, e.g. `python3 -m venv bank-statement-analyzer-venv`
3. Activate virtual environment, e.g. `source bank-statement-analyzer-venv/bin/activate`
4. Install packages - `pip install -r requirements.txt`

## Supported Bank/Credit Card CSVs
* American Express
* Capital One
* Chase
* Discover
* Nordstrom
* Schwab

## Use
1. You will have to manually download CSVs for each bank/card, and put them into a directory.
* Each CSV should be for one bank/card, and should be named with the following convention: yyyy-mm range, bank, and card, e.g. `2023-dec-2024-jan-chase-sapphire.csv` This is critical as file names provide metadata on transactions
2. You must have a Google project set up with a `credentials.json` and service account that can interact with Google Drive and Google Sheets. [Here](https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0) is a helpful article on how to do so
3. Update the `CSV_DIRECTORY`, `SHEET_KEY`, and `WORKSHEET_NAME` variables to wire things up
4. From the project directory, execute `run.py`. Data should now be in the Google Sheet
