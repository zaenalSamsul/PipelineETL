import pandas as pd
import numpy as np
from datetime import datetime
import warnings

# Nonaktifkan peringatan FutureWarning dari pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('future.no_silent_downcasting', True)

def transform_data(products):
    """
    Membersihkan dan mentransformasi data hasil scraping menjadi DataFrame yang siap dianalisis atau disimpan.

    Parameter:
    - products: list of dict, hasil dari fungsi scraping

    Return:
    - df: pandas.DataFrame yang telah dibersihkan dan ditransformasi
    """
    # Konversi list of dict ke DataFrame
    df = pd.DataFrame(products)

    if df.empty:
        print("⚠️ Data kosong. Tidak ada produk yang bisa diproses.")
        return pd.DataFrame()

    # 1. Filter produk yang tidak valid
    df = df[df['title'].str.lower() != 'unknown product']

    # 2. Bersihkan dan konversi harga ke IDR (asumsi 1 USD = 16,000 IDR)
    df['price'] = pd.to_numeric(
        df['price'].str.replace(r'[^\d.]', '', regex=True),
        errors='coerce'
    ) * 16000

    # 3. Bersihkan dan konversi rating
    df['rating'] = pd.to_numeric(
        df['rating'].str.replace(r'[^\d.]', '', regex=True),
        errors='coerce'
    )

    # 4. Ekstrak jumlah warna dari teks (misal: 'Colors: 3')
    df['colors'] = pd.to_numeric(
        df['colors'].str.extract(r'(\d+)')[0],
        errors='coerce'
    )

    # 5. Bersihkan string size dan gender
    df['size'] = df['size'].str.replace(r'Size:\s*', '', regex=True).str.strip()
    df['gender'] = df['gender'].str.replace(r'Gender:\s*', '', regex=True).str.strip()

    # 6. Hapus baris dengan data penting yang null
    df.dropna(subset=['price', 'rating', 'colors', 'size', 'gender'], inplace=True)

    # 7. Hapus data duplikat
    df.drop_duplicates(inplace=True)

    # 8. Tambahkan timestamp proses transformasi
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"✅ Transformasi data selesai. Total produk valid: {len(df)}")
    return df
