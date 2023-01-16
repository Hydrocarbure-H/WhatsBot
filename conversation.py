# -*- coding: utf-8 -*-
# @Author: Luca
# @Date:   2023-01-12 23:40:41
# @Last Modified by:   thomas
# @Last Modified time: 2023-01-13 15:00:36


from driver import Driver
from file import File
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from hashlib  import sha256
from datetime import datetime

from discord import DiscordWH
from webhooks import WebHooks

##
## This class describes a conversation.
## @params      contact - The wanted destination to read or
##                        send messages
##
class Conversation:
    def __init__(self, contact):
        self.contact = contact
        # Starting WebDriver
        self.driver = Driver()

        # Reach contact div and select it.
        # Stay at this point while the page is not entirely loaded
        x_contact = "//span[contains(@title, '" + contact + "')]"
        contact_title = self.driver.getWait().until(
            EC.presence_of_element_located((By.XPATH, x_contact))
        )
        contact_title.click()
        time.sleep(5)

        # Selecting conversation side panel
        x_panel = "//div[contains(@data-testid, 'conversation-panel-messages')]"
        self.__panel = self.driver.getDriver().find_element(By.XPATH, x_panel)

    ##
    ## Gets the messages.
    ##
    ## :returns:   The list of messages as a dict format.
    ## :rtype:     { <List<Dict{date, author, text}>> }
    ##
    def __get_messages(self):

        # Preparing selectors path
        x_container = ".//div[contains(@data-testid, 'msg-container')]"
        x_message = ".//span[contains(@class, 'copyable-text')]"
        x_metadata = ".//div[contains(@class, 'copyable-text')]"
        x_response = ".//div[contains(@data-testid, 'quoted-message')]"
        x_response_text = ".//div/div/span[contains(@class, 'quoted-mention')]"
        x_response_author = ".//div/div/span[not(contains(@class, 'quoted-mention'))]"
        
        messages = self.__panel.find_elements(By.XPATH, x_container)
        messages_list = []

        # Walk along messages received from selection
        # Note : message is a WebElement object
        for message in messages:
            # Trying to get the body message, the date and the author
            try:
                text = message.find_element(By.XPATH, x_message).text
                metadata = message.find_element(By.XPATH, x_metadata).get_attribute(
                    "data-pre-plain-text"
                )
                date_str = metadata[metadata.index("[") + 1 : metadata.index("]")]
                author = metadata[
                    metadata.index("]")
                    + 2 : metadata.index(":", metadata.index(":") + 1)
                ]

                try:
                    response_container = message.find_element(By.XPATH, x_response)
                    response_text = response_container.find_element(By.XPATH, x_response_text).text
                    response_author = response_container.find_element(By.XPATH, x_response_author).text

                    response = {"author": response_author, "text": response_text}

                except NoSuchElementException:
                    response = None

                # Parsing the date
                date = datetime.strptime(date_str, "%H:%M, %d/%m/%Y")
                messages_list.append({"date": date, "author": author, "text": text, "response": response})

            # Note : img elements are currently not recognized
            # So theses errors are handled by NoSuchElementException
            except NoSuchElementException:
                continue

        return messages_list

    ##
    ## Format the date, check if this is today or another day in the week
    ##
    ## :param      date:  The date
    ##
    ## :returns:   { The formatted date }
    ##
    @staticmethod
    def __format_date(date):
        if date.date() == datetime.today().date():
            return date.strftime("%H:%M")
        return date.strftime("%d/%m/%Y %H:%M")

    ##
    ## Reads the last messages which are stored into messages list.
    ##
    def read_last_messages(self):
        messages = self.__get_messages()
        file = File()
        old_hash = file.read()
        new_hash = ""
        index = 0

        for idx,message in enumerate(messages):

            hash_string = (
                        str(message['date'].timestamp()) 
                        + message['author'] 
                        + message['text']
                        )

            if(message['response'] != None):   
                hash_string += message['response']['author'] + message['response']['text']
            
            new_hash = sha256(hash_string.encode('utf-8')).hexdigest()

            if(new_hash == old_hash):
                index = idx

        del messages[0:index + 1]

        for message in messages:

            if(message["response"] != None):
                print("In response to : [" + message["response"]["author"] + " : " + message["response"]["text"] + "] : ", end = '')

            print(
                Conversation.__format_date(message["date"])
                + " "
                + message["author"]
                + " : "
                + message["text"]
            )

            Discord = None

            sws_code = Conversation.is_sws_code(message['text'])

            # Check if this is a SWS code.
            if ( sws_code != None ):                
                Discord = DiscordWH(
                    WebHooks.WHATSAPP.value, sws_code, message["author"], True
                )

            else:
                # TODO send response message and author if any
                Discord = DiscordWH(
                    WebHooks.WHATSAPP.value, message["text"], message["author"]
                )

            #Discord.execute()
            #time.sleep(2)

        if(len(messages) > 0):
            hash_string = (
                str(messages[len(messages) - 1]['date'].timestamp()) 
                + messages[len(messages) - 1]['author'] 
                + messages[len(messages) - 1]['text']
                )

            if(messages[len(messages) - 1]['response'] != None):   
                hash_string += messages[len(messages) - 1]['response']['author'] + messages[len(messages) - 1]['response']['text']

            file.write(sha256(hash_string.encode('utf-8')).hexdigest()) 

    ##
    ## Sends a message.
    ##
    ## :param      message:  The message
    ## :type       message:  String
    ##
    def send_message(self, message):
        # Selecting typing area
        x_input = "//div[contains(@title, 'Type a message')]"
        input_box = self.__panel.find_element(By.XPATH, x_input)
        input_box.send_keys(message + Keys.ENTER)
        time.sleep(2)

    ##
    ## check if text contains sws code.
    ##
    ## :returns:   The sws code.
    ## :rtype:     { String, None }
    ##
    @staticmethod
    def is_sws_code(message):
        good = False
        code = ""
        # Walk along each character to check if it has the NNNNN format
        for c in message:
            if c.isdigit():
                code += c
            elif len(code) < 5:
                code = ""

            if len(code) == 5:
                good = True
            elif len(code) > 5:
                good = False
        if good:
            return code
        return None
