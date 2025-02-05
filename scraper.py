# scraper.py

import os
import requests
from bs4 import BeautifulSoup
from utils import random_delay, sanitize_filename
from csv_handler import log_to_csv
from config import BASE_URL, OUTPUT_DIR, MAX_RETRIES, TIMEOUT

def download_pdf(pdf_url, output_dir, file_name, retries=MAX_RETRIES):
    """Download the PDF from the given URL."""
    attempts = 0
    while attempts < retries:
        try:
            print(f"Downloading PDF from {pdf_url}")
            response = requests.get(pdf_url, timeout=TIMEOUT)
            response.raise_for_status()
            pdf_path = os.path.join(output_dir, file_name)
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(f"Saved PDF: {pdf_path}")
            return True
        except requests.exceptions.Timeout:
            print(f"Timeout error while downloading PDF: {pdf_url}. Retrying...")
        except Exception as e:
            print(f"Failed to download PDF from {pdf_url}: {e}. Retrying...")
        attempts += 1
        random_delay()
    return False

def process_paper(paper_url, base_url, output_dir, csv_file):
    """Process a paper page to extract and download the PDF."""
    try:
        print(f"Processing paper: {paper_url}")
        paper_page = requests.get(paper_url, timeout=TIMEOUT)
        paper_page.raise_for_status()
        soup = BeautifulSoup(paper_page.text, 'html.parser')

        paper_title = soup.title.text.strip() if soup.title else "No Title"
        sanitized_title = sanitize_filename(paper_title)

        pdf_link = soup.select_one('a[href$="Paper-Conference.pdf"]')
        if pdf_link:
            pdf_url = base_url + pdf_link['href']
            if download_pdf(pdf_url, output_dir, sanitized_title + ".pdf"):
                log_to_csv(csv_file, paper_title, pdf_url, os.path.join(output_dir, sanitized_title + ".pdf"))
        else:
            print(f"No PDF found for {paper_url}. Skipping.")
    except Exception as e:
        print(f"Error processing paper {paper_url}: {e}. Skipping.")

def scrape_year_page(year_url, base_url, output_dir, csv_file):
    """Scrape the year archive page for links to individual papers."""
    try:
        print(f"Connecting to year page: {year_url}")
        year_page = requests.get(year_url, timeout=TIMEOUT)
        year_page.raise_for_status()
        soup = BeautifulSoup(year_page.text, 'html.parser')

        paper_links = soup.select('ul.paper-list li a[href$="Abstract-Conference.html"]')
        print(f"Found {len(paper_links)} papers on {year_url}")

        # Process each paper link
        for paper_link in paper_links:
            paper_url = base_url + paper_link['href']
            process_paper(paper_url, base_url, output_dir, csv_file)

    except Exception as e:
        print(f"Error processing year page {year_url}: {e}. Skipping.")

def scrape_main_page(base_url, output_dir, csv_file):
    """Scrape the main page to get the year archive links."""
    try:
        print(f"Connecting to main page: {base_url}")
        main_page = requests.get(base_url, timeout=TIMEOUT)
        main_page.raise_for_status()
        soup = BeautifulSoup(main_page.text, 'html.parser')

        year_links = soup.select('a[href^="/paper_files/paper/"]')
        print(f"Found {len(year_links)} year archive links on the main page.")

        for year_link in year_links:
            year_url = base_url + year_link['href']
            scrape_year_page(year_url, base_url, output_dir, csv_file)

    except Exception as e:
        print(f"Error processing main page {base_url}: {e}. Skipping.")
