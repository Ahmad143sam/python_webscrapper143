# utils.py

import time
import random

def random_delay(min_delay=4, max_delay=70):
    """Introduce a random delay between requests to avoid overloading the server."""
    delay = random.uniform(min_delay, max_delay)
    print(f"Waiting for {delay:.2f} seconds.")
    time.sleep(delay)

def sanitize_filename(filename):
    """Sanitize the filename by replacing invalid characters with underscores."""
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
