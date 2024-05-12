import json

class JsonParser:
    def __init__(self):
        self.json = ""
        self.formattedDict = {}

    def feed_data(self, data):
        self.json = data
        self.formattedDict = json.loads(self.json)
        return self.formattedDict
