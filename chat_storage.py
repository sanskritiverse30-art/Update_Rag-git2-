import json
import os

FILE = "chats.json"


class ChatStorage:
    def __init__(self):
        if not os.path.exists(FILE):
            with open(FILE, "w") as f:
                json.dump({}, f)

    def load(self):
        with open(FILE, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(FILE, "w") as f:
            json.dump(data, f, indent=2)

    def update(self, sessions):
        self.save(sessions)