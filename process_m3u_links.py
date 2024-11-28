import os
import re
import requests
from pprint import pprint

def get_domain(url):
    """Extract the domain from the URL."""
    match = re.match(r'(https?://[^/]+)', url)
    if match:
        return match.group(1)
    return None

def fetch_data(url):
    """Fetch data from the URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from the URL: {e}")

def process_m3u8_data(url):
    """Process m3u8 data and return a list of complete URLs."""
    main_domain = get_domain(url)
    if not main_domain:
        raise ValueError("Invalid URL provided; unable to extract domain.")

    raw_data = fetch_data(url)
    main_urls = []

    # Splitting data into lines and filtering out comments and empty lines
    data_lines = [line.strip() for line in raw_data.split("\n") if line.strip() and not line.startswith("#")]

    url_pattern_with_http = re.compile(r'(https?://[^\s]+)')

    for line in data_lines:
        if url_pattern_with_http.match(line):
            main_urls.append(line)
        else:
            if not main_domain:
                raise RuntimeError("Domain name is empty, and the URL is not absolute.")

            # Validate the domain
            if not url_pattern_with_http.match(main_domain):
                raise ValueError("Domain name is not a valid URL.")

            # Append relative URLs to the main domain
            main_urls.append(f"{main_domain}{line}")

    return main_urls

if __name__ == "__main__":
    url = '<URL>.m3u8'

    try:
        main_urls = process_m3u8_data(url)
        pprint(main_urls)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")
