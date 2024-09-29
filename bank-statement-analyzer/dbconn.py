import pandas as pd
import sqlite3

def update_db(new_df):
    table_exists = table_already_exists()

    if table_exists:
        print("table exists, pulling and merging data")
        existing_df = get_existing_data()
        insert_df = pd.concat(
            [existing_df,
             new_df[ ~new_df['transaction_id'].isin(existing_df['transaction_id'])],
            ]
        )
 
    else:
        print("table does not exist, adding data")
        insert_df = new_df

    conn = sqlite3.connect('personal_finance.db')
    insert_df.to_sql('statement_transactions', conn, if_exists='replace', index=False)


def table_already_exists():
    check_conn = sqlite3.connect('personal_finance.db')
    cursor = check_conn.cursor()
    cursor.execute("PRAGMA table_info(statement_transactions)")
    result = cursor.fetchone()
    check_conn.close()

    if result is not None:
        return True
    else:
        return False


def get_existing_data():
    read_conn = sqlite3.connect('personal_finance.db')
    existing_df = pd.read_sql_query("SELECT * from statement_transactions", read_conn)
    read_conn.close()
    return existing_df

