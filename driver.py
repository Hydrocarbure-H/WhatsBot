from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class Driver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=/WhatsappBot-data")
        # Delete Automation detection flag
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--output=/dev/null")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-site-isolation-trials")
        # chrome_options.add_argument("--enable-low-end-device-mode")
        # chrome_options.add_argument("--max_old_space_size=330")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        )
        self.__driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', options=chrome_options)
        self.__driver.get("https://web.whatsapp.com")
        self.__wait = WebDriverWait(self.__driver, 600)

    def __del__(self):
        self.__driver.quit()

    def getDriver(self):
        return self.__driver

    def getWait(self):
        return self.__wait
