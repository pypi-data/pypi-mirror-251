import requests

class Webhook():
    def __init__(self):
        self.username = None
        self.avatar_url = None
        self.webhook_url = None
        self.embeds = []
        self.content = None
    def send(self):
        json = {}
        if self.username is not None:
            json["username"] = self.username
        if self.content is not None:
            json["content"] = self.content
        if self.avatar_url is not None:
            json["avatar_url"] = self.avatar_url
        if self.embeds is not []:
            json["embeds"] = self.embeds
        result = requests.post(self.webhook_url, json=json)
        return result