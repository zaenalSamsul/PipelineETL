import requests
from bs4 import BeautifulSoup

def scrape_main(url):
    """
    Mengambil data produk dari halaman web yang diberikan URL-nya.
    Mengembalikan list berisi dictionary informasi setiap produk.
    """
    try:
        # Ambil konten HTML dari URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Naikkan error jika status bukan 200 OK
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gagal mengakses URL: {url}\nDetail: {e}")

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_cards = soup.find_all('div', class_='collection-card')

        results = []

        for card in product_cards:
            # Ambil informasi produk
            title = card.find('h3', class_='product-title')
            price = card.find('div', class_='price-container')
            rating = card.find('p', string=lambda t: t and 'Rating' in t)
            colors = card.find('p', string=lambda t: t and 'Colors' in t)
            size = card.find('p', string=lambda t: t and 'Size' in t)
            gender = card.find('p', string=lambda t: t and 'Gender' in t)

            # Masukkan data ke dalam dictionary
            product_info = {
                'title': title.text.strip() if title else 'Unknown Title',
                'price': price.text.strip() if price else 'Price Unavailable',
                'rating': rating.text.strip() if rating else 'No Rating',
                'colors': colors.text.strip() if colors else 'No Color Info',
                'size': size.text.strip() if size else 'No Size Info',
                'gender': gender.text.strip() if gender else 'No Gender Info'
            }

            results.append(product_info)

        return results

    except Exception as e:
        raise Exception(f"Gagal melakukan parsing HTML.\nDetail: {e}")
