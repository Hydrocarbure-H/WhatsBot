from auth import *
from driver import *


def get_message_dict(message, index):
    msg_elem = dict()
    msg_elem["author"] = ""
    msg_elem["body"] = ""
    msg_elem["time"] = ""
    last_author = ""
    msg_web = ""
    msg_web_splitted = ""
    # Author
    try:
        msg_web = message.find_element(
            By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[' + str(index) + ']').text
    except:
        print("Error during getting the message element.")

    try:
        msg_web_splitted = msg_web.split("\n")
    except:
        print("Error while parsing this message element : " + msg_web)

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
        index -= 1
        return (None, index)

    return (msg_elem, index)


def get_last_messages(destination_name, driver):
    # Load cookies
    load_cookie(driver, "cookies.pkl")

    for i in range(5):
        # Get the destination area
        try:
            destination = driver.find_element(
                By.XPATH, "//span[.='" + destination_name + "']")
            destination.click()
        except:
            print("Destination not found")

        # Get the messages list
        try:
            messages_list = driver.find_elements(By.CLASS_NAME, "_22Msk")
        except:
            print("Messages list not found")

        clean_messages_list = []
        index = len(messages_list) + 1

        # Parse all messages from the list
        for message in messages_list:
            # Create msg_elem
            # Structure : { "author" : "author", "body" : "body", "time" : "time" }
            msg_elem, index = get_message_dict(message, index)

            # If the message is not valid, skip it
            if (msg_elem == None):
                continue

            # Add the message to the clean messages list
            clean_messages_list.append(msg_elem)
            index -= 1

        print("Messages : " + str(len(clean_messages_list)))
        sleep(3)

    # Save cookies
    save_cookie(driver, "cookies.pkl")
    return clean_messages_list
