import time
from colorama import Fore, Style
from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql

def scrape_page(url, retries=3):
    """Scrape a single page with retry mechanism."""
    for attempt in range(1, retries + 1):
        try:
            print(f"{Fore.BLUE}[Attempt {attempt}] Scraping: {url}{Style.RESET_ALL}")
            return scrape_main(url)
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to scrape {url} on attempt {attempt}: {e}{Style.RESET_ALL}")
            time.sleep(2)  # Wait before retrying
    print(f"{Fore.YELLOW}⚠️ Skipping {url} after {retries} failed attempts.{Style.RESET_ALL}")
    return []

def main():
    base_url = 'https://fashion-studio.dicoding.dev/'
    all_products = []

    print(f"{Fore.CYAN}Starting scraper for: {base_url}{Style.RESET_ALL}")

    # Scrape the main page (without /page)
    print(f"{Fore.GREEN}Scraping main page: {base_url}{Style.RESET_ALL}")
    all_products.extend(scrape_page(base_url))

    # Scrape pages 2 to 50
    for page in range(2, 51):
        url = f"{base_url}page{page}"
        print(f"{Fore.GREEN}Scraping page {page}: {url}{Style.RESET_ALL}")
        all_products.extend(scrape_page(url))

    # Transform data
    print(f"{Fore.MAGENTA}Transforming data...{Style.RESET_ALL}")
    transformed_data = transform_data(all_products)

    # Save data to CSV
    print(f"{Fore.YELLOW}Saving data to CSV...{Style.RESET_ALL}")
    save_to_csv(transformed_data)

    # Load data to PostgreSQL
    print(f"{Fore.YELLOW}Loading data to PostgreSQL...{Style.RESET_ALL}")
    load_to_postgresql(transformed_data)

    # Save to Google Sheets
    print(f"{Fore.YELLOW}Saving data to Google Sheets...{Style.RESET_ALL}")
    save_to_google_sheets(
        transformed_data,
        '1usfdnQzhMZPLcES3sMVkbbbvvC__BMTNzZHwcblziZE',
        'Sheet1!A2'
    )

    print(f"{Fore.CYAN}Scraping completed successfully!{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
