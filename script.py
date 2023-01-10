from auth import *
from driver import *
from functions import *

driver = driver()
driver.get("https://web.whatsapp.com/")

driver.implicitly_wait(5)

for i in range(20):
    try:
        destination = driver.find_element(By.XPATH, "//span[.='L3-RS2']")
        destination.click()
    except:
        print("Destination not found")

    try:
        messages_list = driver.find_elements(By.CLASS_NAME, "_22Msk")
    except:
        print("Messages list not found")

    clean_messages_list = []
    counter = len(messages_list)
    last_author = ""

    for message in messages_list:
        msg_elem = dict()
        msg_elem["author"] = ""
        msg_elem["message"] = ""
        msg_elem["time"] = ""
        # Author
        try:
            msg_elem["author"] = message.find_element(
                By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[' + str(counter) + ']/div/div/div[2]/div[1]/div[1]').text
            last_author = msg_elem["author"]
        except:
            print("Error during parsing the author.")

        # First message
        # //*[@id="main"]/div[2]/div/div[2]/div[3]/div[33]/div/div/div[2]/div[1]/div[2]/div/span[1]/span
        # second message
        # //*[@id="main"]/div[2]/div/div[2]/div[3]/div[34]/div/div/div[1]/div[1]/div[1]/div/span[1]/span

        # First message before quoted message
        # //*[@id="main"]/div[2]/div/div[2]/div[3]/div[32]/div/div/div[1]/div[1]/div[2]/div[2]/span[1]/span
        # Quoted message
        # //*[@id="main"]/div[2]/div/div[2]/div[3]/div[32]/div/div/div[1]/div[1]/div[2]/div[1]/div/div/div/div

        print("[" + msg_elem["author"] + "] \n")

        try:
            msg_elem["message"] = message.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[' + str(
                counter) + ']/div/div/div[2]/div[1]/div[2]/div/span[1]/span').text
        except:
            try:
                msg_elem["message"] = message.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[' + str(
                    counter + 1) + ']/div/div/div[1]/div[1]/div[1]/div/span[1]/span').text
            except:
                print("Error during parsing the message.")

        # msg_elem["time"] = message.find_element(By.XPATH, '// *[@id="main"]/div[2]/div/div[2]/div[3]/div[' + str(
        #     counter) + ']/div/div/div[1]/div[1]/div[2]/div/span').text

        print("Message : " + msg_elem["message"] + "\n")
        # msg_elem["author"] = (message.find_elements(
        #     By.CLASS_NAME, "a71At"))[0].text
        # # Message
        # msg_elem[1] = (message.find_elements(By.CLASS_NAME, "i0jNr"))[0].text
        # # Time
        # msg_elem[2] = (message.find_elements(
        #     By.CLASS_NAME, "tvf2evcx"))[0].text
        clean_messages_list.append(msg_elem)
        counter -= 1

    print("Messages list length : " + str(len(messages_list)))
    print("Clean messages list length : " + str(len(clean_messages_list)))

    sleep(2)

# Get cookies
save_cookie(driver, "cookies.pkl")

driver.quit()
