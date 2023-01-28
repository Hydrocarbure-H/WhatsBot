# -*- coding: utf-8 -*-
# @Author: thomas
# @Date:   2023-01-13 00:22:21
# @Last Modified by:   thomas
# @Last Modified time: 2023-01-13 14:58:18

from discord_webhook import DiscordWebhook, DiscordEmbed


class DiscordWH:
    def __init__(self, webhook, message, author, date, is_code_sws=False, ping=""):
        self.webhook = webhook
        self.message = message
        self.webhook_content = ""
        self.author = author
        self.code_sws = is_code_sws
        self.ping = ping
        self.color = "21d968"
        self.date = date

        # Specific use for SoWeSign code
        if self.code_sws:
            self.color = "fffefe"
            self.webhook_content = "@everyone"

        if self.ping != "":
            self.color = "33ACFF"
            self.webhook_content = "@"+ self.ping

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
        if self.ping != "":
            embed = DiscordEmbed(
                title="Mention", description=self.message, color=self.color
            )
        else:
            embed = DiscordEmbed(description=self.message, color=self.color)

        # set timestamp (default is now)
        embed.set_timestamp(self.date)

        # add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()
