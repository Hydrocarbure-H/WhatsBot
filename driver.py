from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def driver():

    driver = webdriver.Chrome(options=browser_options())
    options = Options()
    options.add_argument("--user-data-dir=selenium")

    return driver


def browser_options():
    global browser
    option = webdriver.ChromeOptions()
    # Delete Automation detection flag
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("user-data-dir=selenium")  # Store cookies
    # option.add_argument("window-size=1920,1080")
    option.add_argument("--mute-audio")
    option.add_argument("--disable-logging")
    option.add_argument("--log-level=3")
    # option.add_argument("--output=/dev/null")
    # option.add_argument('--headless')
    # option.add_argument("--disable-gpu")
    # option.add_argument("--disable-site-isolation-trials")
    # option.add_argument("--enable-low-end-device-mode")
    # option.add_argument("--max_old_space_size=330")
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36")
    return option  # Apply previous options
