import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from plyer import notification

# List of websites to monitor
URLS = [
    "https://example.com",  # Replace with actual URLs
    "https://another-example.com"
]

# Keywords to search for
KEYWORDS = ["update", "new release", "discount"]

# Dictionary to store previous page content
page_content_cache = {}

# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def get_page_content(url):
    """Fetches and returns the text content of a given URL using Selenium."""
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully load
        return driver.page_source.lower()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def check_for_keywords(content, keywords):
    """Checks if any keyword is present in the webpage content."""
    return any(keyword.lower() in content for keyword in keywords)

def send_notification(message):
    """Sends a desktop notification."""
    notification.notify(
        title="Website Monitor Alert",
        message=message,
        timeout=10
    )

def monitor_websites():
    """Monitors the websites for keyword occurrences and page refresh."""
    while True:
        for url in URLS:
            content = get_page_content(url)
            if content:
                # Check if page content has changed
                if url in page_content_cache and page_content_cache[url] != content:
                    # Check for keywords
                    if check_for_keywords(content, KEYWORDS):
                        send_notification(f"Keyword found on {url}")
                        print(f"Keyword found on {url}!")

                # Update cache
                page_content_cache[url] = content

        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    print("Monitoring websites...")
    monitor_websites()
