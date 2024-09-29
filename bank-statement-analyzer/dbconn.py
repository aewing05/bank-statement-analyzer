import pandas as pd
import sqlite3


def update_db(new_df):
    conn = sqlite3.connect('personal_finance.db')
    existing_df = pd.read_sql_query("SELECT * from statement_transactions", conn)

    merged_df = pd.concat(
        [existing_df,
         new_df[ ~new_df['transaction_id'].isin(existing_df['transaction_id'])],
        ]
    )

    merged_df.to_sql('statement_transactions', conn, if_exists='replace', index=False)

    conn.close()

