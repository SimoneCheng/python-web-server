from parser.buffer import Buffer
from parser.form_data_parser import FormDataParser

class HttpRequestParser:
    def __init__(self):
        self.buffer = Buffer()
        self.done_parsing_firstline = False
        self.done_parsing_header = False
        self.done_parsing_body = False
        self.expected_body_length = 0
        self.parsed_data = {}

    def feed_data(self, data):
        self.buffer.feed_data(data)
        self.parse()
        return self.parsed_data

    def parse(self):
        while not self.done_parsing_firstline:
            self.parse_firstline()
        while not self.done_parsing_header:
            self.parse_header()
        while not self.done_parsing_body:
            self.parse_body()

    def parse_firstline(self):
        first_line = self.buffer.pop(separator="\r\n")
        if first_line is not None:
            http_method, url, http_version = first_line.split()
            self.parsed_data.update({
                "http-method": http_method,
                "url": url,
                "http-version": http_version
            })
            self.done_parsing_firstline = True

    def parse_header(self):
        line = self.buffer.pop(separator="\r\n")
        if line is not None:
            if line:
                name, value = line.split(": ", maxsplit=1)
                if name.lower() == "content-length":
                    self.expected_body_length = int(value)
                self.parsed_data.update({ name.lower(): value })
            else:
                self.done_parsing_header = True
        else:
            self.done_parsing_header = True

    def parse_body(self):
        data = self.buffer.popAll()
        self.expected_body_length = len(data)
        content_type, rest = self.parsed_data['content-type'].split('; ')
        if content_type == 'multipart/form-data':
            form_data_parser = FormDataParser()
            boundary = '--' + rest[9:] # 感覺不是一個好方法
            body = form_data_parser.feed_data(data[len(boundary):], boundary)
            self.parsed_data.update({ 'body': body })
        self.done_parsing_body = True
