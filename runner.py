# runner.py

# Import the necessary modules in the correct sequence
from config import BASE_URL, OUTPUT_DIR, CSV_FILE
from csv_handler import initialize_csv, log_to_csv
from utils import random_delay
from scraper import scrape_main_page
import os

def run_all():
    # Step 1: Initialize CSV file for logging
    print("Initializing CSV file...")
    initialize_csv(CSV_FILE)

    # Step 2: Create the output directory if it doesn't exist
    print(f"Ensuring output directory exists: {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 3: Start the scraping process
    print("Starting scraping process...")
    scrape_main_page(BASE_URL, OUTPUT_DIR, CSV_FILE)

if __name__ == '__main__':
    run_all()
