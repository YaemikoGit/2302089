from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import logging

BASE_URL = "http://localhost:5000"  # Flask app must be running

# Set up logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("selenium_test.log"),
        logging.StreamHandler()
    ]
)

# Configure headless Chrome with console logging enabled
def get_driver():
    caps = DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {"browser": "ALL"}  # Enable browser console logs

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service()  # Can optionally specify chromedriver path here
    driver = webdriver.Chrome(service=service, options=options, desired_capabilities=caps)
    return driver

# Define test cases
test_cases = [
    {
        "description": "Test valid input",
        "input": "hello world",
        "expected_url_contains": "/result",
        "expected_text": "hello world"
    },
    {
        "description": "Test XSS input",
        "input": "<script>alert('XSS')</script>",
        "expected_url_contains": "/",
        "expected_text": "Possible XSS attack detected."
    },
    {
        "description": "Test SQL Injection input",
        "input": "' OR '1'='1",
        "expected_url_contains": "/",
        "expected_text": "Possible SQL Injection detected."
    }
]

def run_tests():
    driver = get_driver()

    for test in test_cases:
        logging.info(f"Running: {test['description']}")
        driver.get(BASE_URL)

        # Fill form
        input_box = driver.find_element(By.NAME, "search_term")
        input_box.clear()
        input_box.send_keys(test['input'])

        # Submit
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)

        # Capture results
        current_url = driver.current_url
        page_source = driver.page_source
        logs = driver.get_log("browser")

        # Print browser console logs
        if logs:
            logging.info("Browser console logs:")
            for entry in logs:
                logging.info(f" - [{entry['level']}] {entry['message']}")

        # Validate result
        if test["expected_url_contains"] in current_url and test["expected_text"] in page_source:
            logging.info(f"✅ Passed: {test['description']}")
        else:
            logging.error(f"❌ Failed: {test['description']}")
            logging.error(f"    URL: {current_url}")
            logging.error(f"    Expected text: {test['expected_text']}")
            logging.error(f"    Page contains: {'Yes' if test['expected_text'] in page_source else 'No'}")

        logging.info("-----")

    driver.quit()

