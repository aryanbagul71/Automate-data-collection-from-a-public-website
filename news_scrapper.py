import requests
from bs4 import BeautifulSoup
import datetime

# The URL of the news website we want to scrape
URL = "https://www.bbc.com/news"
FILE_NAME = "headlines.txt"

# --- CHANGE 1: Add headers to mimic a browser ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Use the headers in the request
    print("Fetching news from BBC...")
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # --- CHANGE 2: Look for both h2 and h3 tags ---
    # This makes our search more flexible
    headlines = soup.find_all(['h2', 'h3'])
    
    # Filter out any potential empty or non-headline tags
    headline_texts = [h.get_text().strip() for h in headlines if len(h.get_text().strip()) > 15]

    if not headline_texts:
        print("Could not find any headlines. The website structure may have changed.")
    else:
        print(f"Saving {len(headline_texts)} headlines to {FILE_NAME}...")
        with open(FILE_NAME, 'w', encoding='utf-8') as file:
            file.write(f"Top Headlines from BBC News ({datetime.date.today()})\n")
            file.write("="*50 + "\n\n")
            for index, title in enumerate(headline_texts, 1):
                file.write(f"{index}. {title}\n")

        print("Scraping complete! ✨")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
except Exception as e:
    print(f"An error occurred: {e}")