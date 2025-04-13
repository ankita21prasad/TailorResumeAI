# backend/cognitive_layers/memory.py
import json

class Memory:
    def __init__(self, filepath="user_data.json"):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def store(self, key, value):
        self.data[key] = value
        self.save_data()

    def retrieve(self, key):
        return self.data.get(key)