import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransformData(unittest.TestCase):
    """
    Unit test untuk fungsi transform_data dari modul utils.transform.
    """

    def test_transform_data_success(self):
        """Test transformasi data valid menghasilkan DataFrame dengan kolom dan nilai yang sesuai."""
        # --- Arrange ---
        products = [
            {
                'title': 'Product 1',
                'price': '$10',
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Product 2',
                'price': '$20',
                'rating': 'Rating: 5.0',
                'colors': 'Colors: 4',
                'size': 'Size: L',
                'gender': 'Gender: Men'
            }
        ]

        # --- Act ---
        df = transform_data(products)

        # --- Assert ---
        self.assertEqual(len(df), 2, "Jumlah baris tidak sesuai")
        self.assertIn('price', df.columns)
        self.assertIn('rating', df.columns)
        self.assertIn('timestamp', df.columns)
        self.assertGreater(df['price'].iloc[0], 0)
        self.assertGreater(df['rating'].iloc[0], 0)

    def test_transform_data_with_invalid_price(self):
        """Test transformasi data gagal karena price tidak valid, hasilkan DataFrame kosong."""
        # --- Arrange ---
        products = [{
            'title': 'Product 1',
            'price': 'invalid_price',
            'rating': 'Rating: 4.5',
            'colors': 'Colors: 3',
            'size': 'Size: M',
            'gender': 'Gender: Men'
        }]

        # --- Act ---
        df = transform_data(products)

        # --- Assert ---
        self.assertTrue(df.empty, "DataFrame harus kosong jika price tidak valid")

# Jalankan semua unit test dengan output yang jelas
if __name__ == '__main__':
    unittest.main(verbosity=2)
