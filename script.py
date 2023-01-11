from auth import *
from driver import *
from functions import *


driver = driver()
driver.get("https://web.whatsapp.com/")

driver.implicitly_wait(5)
msg_list = get_last_messages("L3-RS2", driver)
for message in msg_list:
    print("[ " + message["author"] + " ] " +
          message["body"] + " (" + message["time"] + ")")
driver.quit()
