# Proyek ETL Pipeline Data Produk Fashion

Proyek ini adalah implementasi pipeline ETL (Extract, Transform, Load) untuk mengumpulkan, membersihkan, dan memuat data produk fashion dari situs web. Pipeline ini dibangun sebagai bagian dari submission untuk kelas "Belajar Fundamental Pemrosesan Data" oleh Dicoding Indonesia.

Fokus utama proyek ini adalah membangun sistem yang modular, bersih, terstruktur, dan teruji dengan baik.

## Daftar Isi
1.  [Fitur Utama](#fitur-utama)
2.  [Struktur Proyek](#struktur-proyek)
3.  [Tahapan Pipeline ETL](#tahapan-pipeline-etl)
    * [Extract (Ekstraksi)](#extract-ekstraksi)
    * [Transform (Transformasi)](#transform-transformasi)
    * [Load (Pemuatan)](#load-pemuatan)
4.  [Arsitektur & Testing Modular](#arsitektur--testing-modular)
5.  [Teknologi yang Digunakan](#teknologi-yang-digunakan)
6.  [Prasyarat](#prasyarat)
7.  [Konfigurasi](#konfigurasi)
8.  [Cara Menjalankan](#cara-menjalankan)
9.  [Lisensi](#lisensi)
10. [Ucapan Terima Kasih](#ucapan-terima-kasih)

## Fitur Utama
* **Ekstraksi Data Multi-Halaman:** Mengambil data dari halaman utama hingga 50 halaman produk.
* **Mekanisme Retry:** Implementasi retry otomatis (3 kali percobaan) jika terjadi kegagalan saat scraping halaman.
* **Transformasi Data Komprehensif:**
    * Konversi harga dari USD ke IDR.
    * Ekstraksi nilai numerik dari teks (rating, jumlah warna).
    * Pembersihan format teks (ukuran, gender).
    * Penanganan nilai yang hilang (`NaN`) dan data duplikat.
    * Penambahan kolom `timestamp` proses transformasi.
* **Pemuatan Data Multi-Destinasi:**
    * Menyimpan data ke file CSV.
    * Memuat data ke database PostgreSQL.
    * Menyimpan data ke Google Sheets menggunakan Service Account.
* **Desain Modular:** Kode diorganisir ke dalam modul-modul terpisah untuk ekstraksi, transformasi, dan pemuatan.
* **Testing Modular:** Setiap modul memiliki unit test sendiri untuk memastikan fungsionalitas dan keandalan.
* **Logging Konsol Informatif:** Menggunakan `colorama` untuk memberikan feedback visual selama proses berjalan.

## Struktur Proyek

.
├── main.py                 # Skrip utama untuk menjalankan pipeline ETL
├── utils/
│   ├── init.py
│   ├── extract.py          # Modul untuk ekstraksi data dari web
│   ├── transform.py        # Modul untuk transformasi dan pembersihan data
│   └── load.py             # Modul untuk memuat data ke berbagai destinasi
├── tests/                  # Direktori untuk unit tests (disarankan, dari file test_*.py)
│   ├── init.py
│   ├── test_extract.py     # Unit test untuk modul extract
│   ├── test_transform.py   # Unit test untuk modul transform
│   └── test_load.py        # Unit test untuk modul load
├── scrapping-data.json   # File kredensial Service Account Google (JANGAN DI-COMMIT JIKA REPO PUBLIK)
├── products.csv            # Contoh output CSV
└── README.md



## Tahapan Pipeline ETL

Pipeline terdiri dari tiga tahap utama yang diorkestrasi oleh `main.py`:

### Extract (Ekstraksi)
* **Modul:** `utils/extract.py`
* **Deskripsi:** Bertanggung jawab untuk mengambil konten HTML dari URL target (`https://fashion-studio.dicoding.dev/`). Menggunakan `requests` untuk HTTP GET dan `BeautifulSoup` untuk parsing HTML dan mengekstrak informasi produk (judul, harga, rating, warna, ukuran, gender).
* **Output:** List berisi dictionary data mentah produk.

### Transform (Transformasi)
* **Modul:** `utils/transform.py`
* **Deskripsi:** Mengambil list data mentah produk dan mengubahnya menjadi DataFrame Pandas yang bersih dan terstruktur. Proses ini mencakup pembersihan data, konversi tipe, konversi mata uang (USD ke IDR dengan kurs 1 USD = 16,000 IDR), ekstraksi numerik, penanganan duplikat/NaN, dan penambahan kolom `timestamp`.
* **Output:** DataFrame Pandas yang telah ditransformasi.

### Load (Pemuatan)
* **Modul:** `utils/load.py`
* **Deskripsi:** Mengambil DataFrame yang telah ditransformasi dan menyimpannya ke tiga destinasi berbeda:
    1.  **File CSV:** Menggunakan `df.to_csv()`. Nama file default adalah `products.csv`.
    2.  **PostgreSQL:** Menggunakan `SQLAlchemy` dan `psycopg2` untuk terhubung ke database dan `df.to_sql()` untuk memuat data ke tabel `products`. Opsi `if_exists='replace'` digunakan.
    3.  **Google Sheets:** Menggunakan `google-api-python-client` dan kredensial dari file Service Account (`scrapping-data.json`) untuk memperbarui sheet tertentu.
* **Output:** Data tersimpan di CSV, tabel PostgreSQL, dan Google Sheets.

## Arsitektur & Testing Modular
Proyek ini dirancang dengan arsitektur modular untuk memisahkan concerns (Extract, Transform, Load) ke dalam skrip Python masing-masing di bawah direktori `utils/`. Skrip `main.py` bertindak sebagai orchestrator.

**Testing Modular (Pengujian Unit):**
Setiap modul fungsional (`extract.py`, `transform.py`, `load.py`) memiliki file pengujian unitnya sendiri (`test_extract.py`, `test_transform.py`, `test_load.py`). Pengujian ini menggunakan library `unittest` dan `unittest.mock` dari Python untuk memverifikasi perilaku setiap fungsi secara terisolasi. Hal ini memastikan bahwa setiap komponen bekerja dengan benar sebelum diintegrasikan dalam pipeline penuh.

## Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python 3.x
* **Web Scraping:**
    * `requests`: Untuk melakukan permintaan HTTP.
    * `BeautifulSoup4`: Untuk parsing HTML.
* **Manipulasi & Analisis Data:**
    * `pandas`: Untuk struktur data DataFrame dan manipulasi data.
    * `numpy`: Digunakan secara implisit oleh Pandas untuk operasi numerik.
* **Database & Integrasi:**
    * PostgreSQL: Sebagai sistem manajemen database relasional.
    * `SQLAlchemy`: ORM untuk berinteraksi dengan database PostgreSQL dari Python.
    * `psycopg2`: Adapter PostgreSQL untuk Python (digunakan oleh SQLAlchemy).
* **Integrasi Google Sheets:**
    * `google-api-python-client`
    * `google-auth`
    * `google-oauth2-service-account`
* **Logging & CLI:**
    * `colorama`: Untuk output konsol berwarna yang informatif.
* **Testing:**
    * `unittest`: Framework pengujian standar Python.
    * `unittest.mock`: Untuk membuat objek tiruan (mocks) selama pengujian.
* **Modul Standar Python:**
    * `time`
    * `datetime`
    * `warnings`

## Prasyarat
* Python 3.7+
* PIP (Python package installer)
* Akses ke server PostgreSQL yang sedang berjalan.
* File kredensial Google Cloud Service Account (`scrapping-data.json`) dengan Google Sheets API diaktifkan.

## Konfigurasi

1.  **Dependensi Python:**
    Sebaiknya buat dan gunakan virtual environment. Instal dependensi dari file `requirements.txt` (Anda perlu membuat file ini berdasarkan impor di skrip Anda):
    ```bash
    pip install requests beautifulsoup4 pandas numpy sqlalchemy psycopg2-binary google-api-python-client google-auth colorama
    ```
    *(Catatan: `psycopg2-binary` adalah paket yang mudah diinstal untuk psycopg2).*

2.  **Database PostgreSQL:**
    * Pastikan server PostgreSQL Anda berjalan.
    * Update detail koneksi (username, password, host, port, database) di dalam fungsi `load_to_postgresql` pada file `utils/load.py`.

3.  **Google Sheets API:**
    * Unduh file JSON kredensial Service Account Anda dan simpan sebagai `scrapping-data.json` di direktori root proyek.
    * Update `spreadsheet_id` dan `range_name` pada pemanggilan fungsi `save_to_google_sheets` di `main.py` sesuai dengan Google Sheet target Anda.

## Cara Menjalankan
📦 INSTALASI DEPENDENCY
----------------------------------------
Jalankan perintah berikut untuk menginstal semua dependency:
> pip install -r requirements.txt


🚀 MENJALANKAN APLIKASI UTAMA
----------------------------------------
Untuk menjalankan aplikasi:
> python main.py


🧪 MENJALANKAN UNIT TEST
----------------------------------------
Menjalankan seluruh unit test yang ada di folder `tests/`:
> python -m unittest discover tests


📊 MENJALANKAN TEST COVERAGE
----------------------------------------
Menjalankan pengujian dengan pelacakan cakupan kode:
> coverage run -m unittest discover tests

Melihat hasil report test coverage secara detail:
> coverage report -m


📄 GOOGLE SHEETS - DATA / DOKUMENTASI
----------------------------------------
Akses file Google Sheets melalui link berikut:
https://docs.google.com/spreadsheets/d/1usfdnQzhMZPLcES3sMVkbbbvvC__BMTNzZHwcblziZE/edit?usp=sharing
