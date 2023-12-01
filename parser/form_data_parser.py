from parser.buffer import Buffer

class FormDataParser:
    def  __init__(self):
        self.buffer = Buffer()
        self.boundary = ""
        self.done_parsing_form_data = False
        self.parsed_data = {}

    def feed_data(self, data, boundary):
        self.buffer.feed_data(data)
        self.boundary = boundary
        self.parse()
        return self.parsed_data

    def parse(self):
        self.parse_form_data()

    def parse_form_data(self):
        while not self.done_parsing_form_data:
            data = self.buffer.pop(self.boundary)
            if data is not None:
                content_disposition, value = data.split('\r\n\r\n')
                name_index = content_disposition.find('name=')
                name = content_disposition[name_index + 5:]
                self.parsed_data.update({ name.strip('"'): value.rstrip('\r\n') })
            else:
                self.done_parsing_form_data = True
