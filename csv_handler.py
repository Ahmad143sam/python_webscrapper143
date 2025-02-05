# csv_handler.py

import csv

def initialize_csv(csv_file):
    """Create a new CSV file and add headers if the file doesn't exist."""
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'PDF URL', 'Saved Path'])  # Headers for CSV
    except Exception as e:
        print(f"Error initializing CSV file: {e}")

def log_to_csv(csv_file, title, pdf_url, saved_path):
    """Log the paper details into the CSV file."""
    try:
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, pdf_url, saved_path])  # Log paper details
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
