class Buffer:
    def __init__(self):
        self.data = ""

    def feed_data(self, data):
        self.data += data

    def pop(self, separator):
        first, *rest = self.data.split(separator, maxsplit=1)
        if not rest:
            return None
        else:
            self.data = separator.join(rest)
            return first

    def popAll(self):
        temp = self.data
        self.data = ""
        return temp
