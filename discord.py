# -*- coding: utf-8 -*-
# @Author: thomas
# @Date:   2023-01-13 00:22:21
# @Last Modified by:   thomas
# @Last Modified time: 2023-01-13 14:58:18

from discord_webhook import DiscordWebhook, DiscordEmbed


class DiscordWH:
    def __init__(self, webhook, message, author, is_code_sws=False):
        self.webhook = webhook
        self.message = message
        self.webhook_content = ""
        self.author = author
        self.code_sws = is_code_sws
        self.color = "21d968"

        # Specific use for SoWeSign code
        if self.code_sws:
            self.color = "fffefe"
            self.webhook_content = "@everyone"

    def execute(self):

        webhook = DiscordWebhook(
            url=self.webhook,
            username=self.author,
            content=self.webhook_content,
        )
        if self.code_sws:
            embed = DiscordEmbed(
                title="Code SWS", description=self.message, color=self.color
            )
        else:
            embed = DiscordEmbed(description=self.message, color=self.color)

        # set timestamp (default is now)
        embed.set_timestamp()

        # add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()

        # try:
        #     return True
        # except:
        #     print("Error while sending message to Discord")
        #     return False
