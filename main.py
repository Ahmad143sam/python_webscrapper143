# main.py

import os
from scraper import scrape_main_page
from csv_handler import initialize_csv
from config import BASE_URL, OUTPUT_DIR, CSV_FILE

def main():
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Initialize the CSV file
    initialize_csv(CSV_FILE)

    # Start scraping
    scrape_main_page(BASE_URL, OUTPUT_DIR, CSV_FILE)

if __name__ == '__main__':
    main()
