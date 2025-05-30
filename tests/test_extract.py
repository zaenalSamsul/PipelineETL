import unittest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_main

class TestScrapeMain(unittest.TestCase):
    """
    Unit test untuk fungsi scrape_main dari modul utils.extract.
    """

    @patch('utils.extract.requests.get')
    def test_scrape_main_success(self, mock_get):
        """
        Test jika scraping berhasil mengembalikan data produk yang valid.
        """
        # --- Arrange ---
        url = "https://fashion-studio.dicoding.dev/"
        mock_html = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">$10</div>
                    <p>Rating: 5 stars</p>
                    <p>Colors: Red, Blue</p>
                    <p>Size: M, L</p>
                    <p>Gender: Unisex</p>
                </div>
            </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        # --- Act ---
        result = scrape_main(url)

        # --- Assert ---
        self.assertIsInstance(result, list, "Hasil scraping harus berupa list.")
        self.assertGreater(len(result), 0, "List hasil scraping tidak boleh kosong.")
        self.assertEqual(result[0]['title'], 'Test Product', "Judul produk tidak sesuai.")

    @patch('utils.extract.requests.get')
    def test_scrape_main_failure(self, mock_get):
        """
        Test jika terjadi error saat akses HTTP (misalnya status code 404).
        """
        # --- Arrange ---
        url = "https://fashion-studio.dicoding.dev/"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        # --- Act & Assert ---
        with self.assertRaises(Exception):
            scrape_main(url)

# Jalankan semua unit test
if __name__ == '__main__':
    unittest.main(verbosity=2)
