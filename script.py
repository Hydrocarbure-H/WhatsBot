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
        msg_elem["body"] = ""
        msg_elem["time"] = ""

        msg_web = ""
        msg_web_splitted = ""
        # Author
        try:
            msg_web = message.find_element(
                By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[' + str(counter) + ']').text
        except:
            print("Error during parsing the message element.")

        try:
            msg_web_splitted = msg_web.split("\n")
        except:
            print("Empty element : " + msg_web)

        if (len(msg_web_splitted) == 3):
            msg_elem["author"] = msg_web_splitted[0]
            msg_elem["body"] = msg_web_splitted[1]
            msg_elem["time"] = msg_web_splitted[2]
            last_author = msg_elem["author"]
        elif (len(msg_web_splitted) == 2):
            msg_elem["author"] = last_author
            msg_elem["body"] = msg_web_splitted[0]
            msg_elem["time"] = msg_web_splitted[1]
        else:
            counter -= 1
            continue

        print("[" + msg_elem["author"] + "] : " +
              msg_elem["body"] + " (" + msg_elem["time"] + ")")
        clean_messages_list.append(msg_elem)
        counter -= 1

    print("Messages list length : " + str(len(messages_list)))
    print("Clean messages list length : " + str(len(clean_messages_list)))

    sleep(2)

# Get cookies
save_cookie(driver, "cookies.pkl")

driver.quit()
