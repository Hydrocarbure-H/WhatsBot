# -*- coding: utf-8 -*-
# @Author: Luca
# @Date:   2023-01-13 00:06:13
# @Last Modified by:   thomas
# @Last Modified time: 2023-01-13 01:05:07


from conversation import Conversation
import time
import sys
import getopt


def args(argv):
    message = None
    recipient = None
    arg_help = "{0} -s \n{0} -r <recipient> \n{0} -w <recipient> -m <message>".format(
        argv[0]
    )

    # Trying to parse given arguments
    try:
        opts, args = getopt.getopt(
            argv[1:], "hsr:w:m:", ["help", "sws=", "read=", "write=", "message="]
        )
    except:
        # Bad usage
        print(arg_help)
        sys.exit(2)

    # Walking along given parsed arguments
    for opt, arg in opts:

        # Help
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)

        # SoWeSign code
        elif opt in ("-s", "--sws"):
            conversation = Conversation("L3-RS2")
            conversation.get_sws_code()
            return

        # Get last messages
        elif opt in ("-r", "--read"):
            recipient = arg

        # Message to send
        elif opt in ("-m", "--message"):
            message = arg

        # Write a message and send it
        elif opt in ("-w", "--write"):
            recipient = arg

    if recipient != None:
        # Create a new conversation
        conversation = Conversation(recipient)

        # Send the given message
        if message != None and len(message) > 0:
            conversation.send_message(message)

        # Read the last sent messages
        elif message == None:
            conversation.read_last_messages()


args(sys.argv)
