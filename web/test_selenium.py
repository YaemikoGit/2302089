import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.mark.parametrize("description,input_text,expected_url_contains,expected_text", [
    ("valid input", "hello world", "/result", "hello world"),
    ("XSS attack", "<script>alert('XSS')</script>", "/", "Possible XSS attack detected."),
    ("SQL injection", "' OR '1'='1", "/", "Possible SQL Injection detected."),
])
def test_input_validation(driver, description, input_text, expected_url_contains, expected_text):
    driver.get(BASE_URL)

    input_box = driver.find_element(By.NAME, "search_term")
    input_box.clear()
    input_box.send_keys(input_text)
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)

    assert expected_url_contains in driver.current_url
    assert expected_text in driver.page_source
