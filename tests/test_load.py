import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql

class TestLoadModule(unittest.TestCase):
    """
    Unit test untuk fungsi-fungsi dalam modul utils.load
    """

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        """Test apakah fungsi save_to_csv memanggil to_csv dengan benar."""
        # --- Arrange ---
        df = pd.DataFrame({'title': ['Product 1'], 'price': [10000]})
        filename = 'test_output.csv'

        # --- Act ---
        save_to_csv(df, filename)

        # --- Assert ---
        mock_to_csv.assert_called_once_with(filename, index=False)

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets(self, mock_creds, mock_build):
        """Test apakah data berhasil dikirim ke Google Sheets."""
        # --- Arrange ---
        df = pd.DataFrame({'title': ['Product 1'], 'price': [100]})
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        spreadsheet_id = 'spreadsheet_id'
        range_name = 'Sheet1!A2'

        # --- Act ---
        save_to_google_sheets(df, spreadsheet_id, range_name)

        # --- Assert ---
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    @patch('utils.load.pd.DataFrame.to_sql')
    @patch('utils.load.create_engine')
    def test_load_to_postgresql(self, mock_create_engine, mock_to_sql):
        """Test apakah data berhasil dikirim ke PostgreSQL menggunakan SQLAlchemy."""
        # --- Arrange ---
        df = pd.DataFrame({'title': ['Product 1'], 'price': [100]})
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        # --- Act ---
        load_to_postgresql(df)

        # --- Assert ---
        mock_to_sql.assert_called_once_with('products', mock_engine, if_exists='replace', index=False)

# Jalankan semua unit test
if __name__ == '__main__':
    unittest.main(verbosity=2)
