import os
from time import sleep
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# replace it with path that contains chromedriver
# os.environ['PATH'] += r"C:\Users\saura\Desktop"
driver = webdriver.Chrome()

driver.get("https://web.whatsapp.com/")

driver.implicitly_wait(20)

for i in range(5000):
    try:
        # replace Friend with your WhatsApp contact
        destination = driver.find_element(By.XPATH, "//span[.='L3-RS2']")
        print("Destination found : " + destination.text)
        destination.click()
    except:
        # replace Friend with your whatsApp contact.
        destination = driver.find_element(By.XPATH, "//span[.='L3-RS2']")
        print("Expect destination")
        destination.click()

    messages_list = driver.find_elements(By.CLASS_NAME, "_1-lf9")

    clean_messages_list = []
    for message in messages_list:
        msg_elem = []
        # Author
        msg_elem[0] = (message.find_elements(By.CLASS_NAME, "a71At"))[0].text
        # Message
        msg_elem[1] = (message.find_elements(By.CLASS_NAME, "i0jNr"))[0].text
        # Time
        msg_elem[2] = (message.find_elements(
            By.CLASS_NAME, "tvf2evcx"))[2].text
        clean_messages_list.append(msg_elem)

    print("Messages list length : " + str(len(messages_list)))
    print("Clean messages list length : " + str(len(clean_messages_list)))

    print(clean_messages_list)

    sleep(10)

# for i in range(5):  # Number of time message will be sent.
#     # Replace "Hi" with whatever message you want to send.
#     msg_area.send_keys("")
#     msg_area.send_keys(Keys.RETURN)


driver.implicitly_wait(60)
