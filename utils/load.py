import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

# Menyimpan DataFrame ke file CSV
def save_to_csv(df, filename="products.csv"):
    df.to_csv(filename, index=False)

# Menyimpan DataFrame ke Google Sheets
def save_to_google_sheets(df, spreadsheet_id, range_name):
    creds = Credentials.from_service_account_file('scrapping-data.json')
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    values = df.values.tolist()
    body = {
        'values': values
    }

    sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

# Menyimpan DataFrame ke PostgreSQL
def load_to_postgresql(df, table_name='products'):
    """
    Menyimpan DataFrame ke dalam tabel PostgreSQL.

    Parameter:
    - df: pandas.DataFrame, data yang ingin disimpan.
    - table_name: str, nama tabel di PostgreSQL (default: 'products').
    """
    username = 'submissionetl'
    password = 'zaenal11'
    host = 'localhost'
    port = '5432'
    database = 'productsdb'

    try:
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Data berhasil disimpan ke PostgreSQL pada tabel '{table_name}'. Jumlah baris: {len(df)}")
    except Exception as e:
        print("❌ Gagal menyimpan ke PostgreSQL.")
        print(f"Error: {e}")
