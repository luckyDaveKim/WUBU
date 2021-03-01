#-*- coding: utf-8 -*-
from slacker import Slacker
from slack import WebClient

class Slack():
    def __init__(self, token):
        self.client = WebClient(token)

    def postMessage(self, channel, msg):
        response = self.client.chat_postMessage(
            channel=channel,
            text=msg
        )

if __name__ == '__main__':

    print("Hello")

    slack = Slack('')
    slack.postMessage('bot_test', 'test message!!!!')
