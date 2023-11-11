class Buffer:
    def __init__(self):
        self.data = ""

    def feed_data(self, data):
        self.data += data

    def pop(self, separator):
        separator_index = self.data.find(separator)
        if separator_index == -1:
            return None
        first_data = self.data[:separator_index]
        rest_data = self.data[separator_index+len(separator):]
        if not rest_data:
            return None
        else:
            self.data = rest_data
            return first_data

    def popAll(self):
        temp = self.data
        self.data = ""
        return temp
